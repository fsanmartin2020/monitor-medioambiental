#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor de Noticias de Derecho Medioambiental Chile
====================================================
Script principal: recorre las 69 fuentes configuradas, extrae noticias
de las últimas 24 horas, las clasifica con Gemini y guarda los resultados.

Uso:
    python scraper/main.py

Variables de entorno requeridas:
    GEMINI_API_KEY  → API key de Google Gemini (tier gratuito funciona)
"""

import json
import os
import re
import sys
import time
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import feedparser
from dateutil import parser as dateutil_parser

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
NOTICIAS_FILE = DATA_DIR / "noticias.json"
HISTORIAL_FILE = DATA_DIR / "historial.json"

# Zona horaria de Chile continental (UTC-3)
CHILE_TZ = timezone(timedelta(hours=-3))

# Ventana de noticias: últimas 24 horas
HORAS_VENTANA = 24

# Artículos por lote enviado a Gemini
BATCH_SIZE = 15

# Máximo de URLs guardadas en historial (evita que el archivo crezca sin límite)
MAX_HISTORIAL_URLS = 8000

# Tiempo de espera entre fuentes (segundos) — para no saturar servidores
PAUSA_ENTRE_FUENTES = 0.8

# Headers genéricos para requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Utilidades de fecha
# ---------------------------------------------------------------------------

MESES_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def parse_fecha(texto: str) -> datetime | None:
    """Intenta convertir un string de fecha a datetime con timezone."""
    if not texto:
        return None
    texto = texto.strip()

    # Intento 1: formato ISO 8601
    try:
        return dateutil_parser.parse(texto, ignoretz=False)
    except Exception:
        pass

    # Intento 2: ISO sin timezone → asumir UTC
    try:
        dt = datetime.fromisoformat(texto.replace("Z", "+00:00"))
        return dt
    except Exception:
        pass

    # Intento 3: "15 de enero de 2024" (formato español)
    m = re.search(r"(\d{1,2})\s+de\s+(\w+)\s+(?:de\s+)?(\d{4})", texto, re.I)
    if m:
        dia, mes_str, anio = int(m.group(1)), m.group(2).lower(), int(m.group(3))
        mes = MESES_ES.get(mes_str)
        if mes:
            try:
                return datetime(anio, mes, dia, tzinfo=timezone.utc)
            except Exception:
                pass

    # Intento 4: delegar a dateutil con ignoretz=True
    try:
        dt = dateutil_parser.parse(texto, ignoretz=True)
        return dt.replace(tzinfo=timezone.utc)
    except Exception:
        pass

    return None


def es_reciente(fecha: datetime | None, horas: int = HORAS_VENTANA) -> bool:
    """True si la fecha es dentro de la ventana configurada."""
    if fecha is None:
        return True  # Sin fecha: incluir y dejar que Gemini filtre
    ahora = datetime.now(timezone.utc)
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha >= (ahora - timedelta(hours=horas))


def fecha_chile_str(fecha: datetime | None) -> str:
    """Devuelve fecha en formato YYYY-MM-DD (hora Chile)."""
    if fecha is None:
        return datetime.now(CHILE_TZ).strftime("%Y-%m-%d")
    if fecha.tzinfo is None:
        fecha = fecha.replace(tzinfo=timezone.utc)
    return fecha.astimezone(CHILE_TZ).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Historial (para evitar duplicados entre días)
# ---------------------------------------------------------------------------

def cargar_historial() -> set:
    """Carga el conjunto de URLs ya procesadas."""
    if HISTORIAL_FILE.exists():
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return set(data.get("urls", []))
        except Exception as e:
            logger.warning(f"No se pudo leer historial.json: {e}")
    return set()


def guardar_historial(historial_anterior: set, nuevas_urls: set) -> None:
    """Combina historial anterior con nuevas URLs y guarda, limitando el tamaño."""
    todas = list(historial_anterior | nuevas_urls)
    # Mantener solo las últimas MAX_HISTORIAL_URLS (las más recientes en el tiempo de inserción)
    if len(todas) > MAX_HISTORIAL_URLS:
        todas = todas[-MAX_HISTORIAL_URLS:]
    data = {
        "urls": todas,
        "ultima_actualizacion": datetime.now(CHILE_TZ).isoformat(),
    }
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Historial actualizado: {len(todas)} URLs guardadas")


def guardar_noticias(noticias: list, gemini_disponible: bool) -> None:
    """Guarda las noticias del día en noticias.json."""
    data = {
        "fecha_actualizacion": datetime.now(CHILE_TZ).isoformat(),
        "total": len(noticias),
        "gemini_disponible": gemini_disponible,
        "noticias": noticias,
    }
    with open(NOTICIAS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"noticias.json guardado con {len(noticias)} noticias")


# ---------------------------------------------------------------------------
# RSS
# ---------------------------------------------------------------------------

def fetch_rss(rss_url: str, nombre: str) -> list:
    """Descarga y parsea un feed RSS. Devuelve lista de artículos recientes."""
    try:
        feed = feedparser.parse(rss_url, request_headers=HEADERS)
        if feed.bozo and not feed.entries:
            return []

        articulos = []
        for entry in feed.entries:
            # Obtener fecha
            fecha_raw = (
                getattr(entry, "published", None)
                or getattr(entry, "updated", None)
            )
            # feedparser también expone *_parsed (struct_time)
            if not fecha_raw:
                parsed = (
                    getattr(entry, "published_parsed", None)
                    or getattr(entry, "updated_parsed", None)
                )
                if parsed:
                    try:
                        fecha_raw = datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()
                    except Exception:
                        pass

            fecha_dt = parse_fecha(fecha_raw)
            if not es_reciente(fecha_dt):
                continue

            url_noticia = entry.get("link", "").strip()
            titulo = entry.get("title", "").strip()
            # Limpiar HTML del título si lo tiene
            if titulo:
                titulo = BeautifulSoup(titulo, "html.parser").get_text(strip=True)

            if url_noticia and titulo and len(titulo) > 10:
                articulos.append({
                    "fuente": nombre,
                    "titular": titulo,
                    "url": url_noticia,
                    "fecha": fecha_chile_str(fecha_dt),
                })

        return articulos

    except Exception as e:
        logger.debug(f"Error RSS {nombre} ({rss_url}): {e}")
        return []


def intentar_rss(fuente: dict) -> list | None:
    """
    Prueba todos los RSS URLs configurados para una fuente.
    Devuelve lista (puede estar vacía) si algún feed fue válido, None si todos fallaron.
    """
    rss_urls = []
    if fuente.get("rss_url"):
        rss_urls.append(fuente["rss_url"])
    rss_urls.extend(fuente.get("rss_urls", []))

    for url in rss_urls:
        try:
            feed = feedparser.parse(url, request_headers=HEADERS)
            if not feed.bozo or feed.entries:
                articulos = fetch_rss(url, fuente["nombre"])
                logger.info(f"  RSS OK ({url}): {len(articulos)} artículos recientes")
                return articulos
        except Exception:
            continue

    return None


# ---------------------------------------------------------------------------
# Scraping genérico
# ---------------------------------------------------------------------------

def _url_absoluta(href: str, base_url: str) -> str:
    """Convierte href relativo a URL absoluta."""
    if href.startswith("http"):
        return href
    return urljoin(base_url, href)


def _es_url_valida(url: str) -> bool:
    """Filtra URLs que no son noticias (imágenes, JS, anclas, etc.)."""
    url_lower = url.lower()
    extensiones_skip = (".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".mp4", ".mp3")
    prefijos_skip = ("javascript:", "mailto:", "tel:", "#")
    return (
        url.startswith("http")
        and not any(url_lower.endswith(e) for e in extensiones_skip)
        and not any(url.startswith(p) for p in prefijos_skip)
    )


def _jsonld_articles(soup: BeautifulSoup, base_url: str, nombre: str) -> list:
    """Extrae artículos de JSON-LD si el sitio lo implementa."""
    articulos = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            raw = script.string or ""
            data = json.loads(raw)
            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                continue
            for item in data:
                tipo = item.get("@type", "")
                if tipo not in ("NewsArticle", "Article", "BlogPosting", "WebPage"):
                    continue
                titulo = item.get("headline", "").strip()
                url_art = item.get("url", "").strip()
                fecha_raw = item.get("datePublished") or item.get("dateModified")
                if not titulo or not url_art:
                    continue
                fecha_dt = parse_fecha(fecha_raw)
                if not es_reciente(fecha_dt):
                    continue
                articulos.append({
                    "fuente": nombre,
                    "titular": BeautifulSoup(titulo, "html.parser").get_text(strip=True),
                    "url": _url_absoluta(url_art, base_url),
                    "fecha": fecha_chile_str(fecha_dt),
                })
        except Exception:
            continue
    return articulos


def _article_tags(soup: BeautifulSoup, base_url: str, nombre: str) -> list:
    """Busca tags <article> o contenedores con clases comunes de noticias."""
    articulos = []
    selectores = [
        "article",
        "[class*='noticia']", "[class*='news-item']", "[class*='post-item']",
        "[class*='card']", "[class*='entry']", "[class*='item-noticia']",
    ]
    elementos = []
    for sel in selectores:
        elementos = soup.select(sel)
        if len(elementos) >= 2:
            break

    for elem in elementos[:30]:
        # Título: buscar h1-h4 o un <a> con texto largo
        title_tag = elem.find(["h1", "h2", "h3", "h4"])
        link_tag = elem.find("a", href=True)
        time_tag = elem.find("time")

        titulo = ""
        if title_tag:
            titulo = title_tag.get_text(strip=True)
        elif link_tag:
            titulo = link_tag.get_text(strip=True)

        if not titulo or len(titulo) < 15:
            continue

        url_art = ""
        if link_tag:
            url_art = _url_absoluta(link_tag["href"], base_url)
        if title_tag:
            inner_link = title_tag.find("a", href=True)
            if inner_link:
                url_art = _url_absoluta(inner_link["href"], base_url)

        if not url_art or not _es_url_valida(url_art):
            continue

        # Fecha
        fecha_dt = None
        if time_tag:
            fecha_dt = parse_fecha(time_tag.get("datetime") or time_tag.get_text(strip=True))
        if fecha_dt and not es_reciente(fecha_dt):
            continue

        articulos.append({
            "fuente": nombre,
            "titular": titulo,
            "url": url_art,
            "fecha": fecha_chile_str(fecha_dt),
            "_tiene_fecha": fecha_dt is not None,
        })

    return articulos


def _links_genericos(soup: BeautifulSoup, base_url: str, nombre: str) -> list:
    """
    Fallback: busca <a> con texto largo, evitando menús y pies de página.
    Sin fecha → se incluyen todos (Gemini filtrará por relevancia).
    """
    articulos = []
    seen = set()

    # Ignorar nav, header, footer
    for tag in soup.find_all(["nav", "header", "footer"]):
        tag.decompose()

    for a in soup.find_all("a", href=True):
        texto = a.get_text(strip=True)
        href = _url_absoluta(a["href"], base_url)

        if not _es_url_valida(href):
            continue
        if href in seen:
            continue
        if len(texto) < 25 or len(texto) > 250:
            continue
        # Evitar links de navegación (muy cortos o con palabras clave de menú)
        skip_words = ["inicio", "home", "contacto", "quiénes somos", "sobre nosotros",
                      "política", "términos", "privacidad", "login", "registrar"]
        if any(w in texto.lower() for w in skip_words):
            continue
        # El href debe pertenecer al mismo dominio base o ser relevante
        base_domain = urlparse(base_url).netloc
        href_domain = urlparse(href).netloc
        if base_domain and href_domain and base_domain not in href_domain and href_domain not in base_domain:
            continue

        seen.add(href)
        articulos.append({
            "fuente": nombre,
            "titular": texto,
            "url": href,
            "fecha": datetime.now(CHILE_TZ).strftime("%Y-%m-%d"),
            "_tiene_fecha": False,
        })

    return articulos[:20]


def scrape_generic(fuente: dict) -> list:
    """
    Scraper genérico que intenta varias estrategias en orden de confiabilidad.
    Devuelve lista de artículos (sin campo _tiene_fecha).
    """
    nombre = fuente["nombre"]
    target_url = fuente.get("noticias_url") or fuente["url"]

    try:
        resp = requests.get(target_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "lxml")

        # Estrategia 1: JSON-LD
        articulos = _jsonld_articles(soup, target_url, nombre)
        if articulos:
            logger.info(f"  Scraping JSON-LD {nombre}: {len(articulos)} artículos")
            return [{k: v for k, v in a.items() if not k.startswith("_")} for a in articulos]

        # Estrategia 2: <article> y contenedores
        articulos = _article_tags(soup, target_url, nombre)
        if len(articulos) >= 2:
            logger.info(f"  Scraping article-tags {nombre}: {len(articulos)} artículos")
            return [{k: v for k, v in a.items() if not k.startswith("_")} for a in articulos]

        # Estrategia 3: links genéricos
        articulos = _links_genericos(soup, target_url, nombre)
        if articulos:
            logger.info(f"  Scraping links {nombre}: {len(articulos)} artículos (sin fecha)")
            return [{k: v for k, v in a.items() if not k.startswith("_")} for a in articulos]

        logger.warning(f"  Scraping {nombre}: sin resultados")
        return []

    except requests.exceptions.Timeout:
        logger.warning(f"  Timeout scraping {nombre}: {target_url}")
        return []
    except requests.exceptions.HTTPError as e:
        logger.warning(f"  HTTP {e.response.status_code} scraping {nombre}")
        return []
    except requests.exceptions.ConnectionError:
        logger.warning(f"  Conexión fallida scraping {nombre}")
        return []
    except Exception as e:
        logger.error(f"  Error inesperado scraping {nombre}: {e}")
        return []


# ---------------------------------------------------------------------------
# Procesamiento de fuentes
# ---------------------------------------------------------------------------

def procesar_fuente(fuente: dict) -> list:
    """Procesa una fuente y devuelve sus artículos."""
    nombre = fuente["nombre"]
    metodo = fuente.get("metodo", "rss")

    if metodo == "rss":
        resultado = intentar_rss(fuente)
        if resultado is not None:
            return resultado
        # Fallback a scraping si RSS no funcionó
        logger.info(f"  RSS falló en {nombre}, usando scraping como fallback…")
        return scrape_generic(fuente)
    else:
        return scrape_generic(fuente)


# ---------------------------------------------------------------------------
# Clasificación con Gemini
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """\
Eres un asistente experto en derecho medioambiental chileno.
Para cada uno de los siguientes titulares de noticias, determina si es \
relevante para un abogado especializado en derecho medioambiental en Chile.

Temas RELEVANTES (incluir):
- Regulación y normativa ambiental (leyes, decretos, reglamentos)
- Contaminación (agua, aire, suelo, ruido)
- Recursos naturales: agua, bosques, pesca, fauna, suelos
- Minería y sus impactos ambientales
- Evaluación de Impacto Ambiental (EIA / DIA / SEIA)
- Sanciones, multas y procesos ante la SMA o tribunales ambientales
- Biodiversidad y áreas protegidas (parques, reservas, humedales)
- Cambio climático: políticas, metas, legislación
- Derecho indígena y territorio en contexto ambiental
- Residuos, RETC, sustancias peligrosas
- Energías renovables y su marco regulatorio
- Acuerdo de Escazú
- Fallos de tribunales ambientales o Corte Suprema en materia ambiental
- Conflictos socioambientales
- Proyectos de inversión sujetos a evaluación ambiental

Temas NO RELEVANTES (excluir):
- Deportes, espectáculos, farándula, cultura
- Política electoral sin relación directa con legislación ambiental
- Economía y finanzas sin relación con recursos naturales
- Tecnología y startups sin componente ambiental
- Noticias sociales generales
- Accidentes de tránsito, delincuencia, salud (salvo contaminación)

Responde ÚNICAMENTE con un array JSON de "si" o "no", uno por titular en el mismo orden.
Ejemplo: ["si","no","si","no","si"]

Titulares:
{titulares}"""


def clasificar_con_gemini(articulos: list) -> tuple[list, bool]:
    """
    Clasifica los artículos usando Gemini.
    Devuelve (lista_relevantes, gemini_disponible).
    Si Gemini no está disponible, devuelve todos los artículos.
    """
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY no configurada — se muestran todas las noticias sin filtrar")
        return articulos, False

    if not articulos:
        return [], True

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        logger.error(f"Error inicializando Gemini: {e}")
        return articulos, False

    relevantes = []
    total_batches = (len(articulos) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_idx, i in enumerate(range(0, len(articulos), BATCH_SIZE), start=1):
        batch = articulos[i : i + BATCH_SIZE]
        titulares_texto = "\n".join(
            f"{j + 1}. {a['titular']}" for j, a in enumerate(batch)
        )
        prompt = PROMPT_TEMPLATE.format(titulares=titulares_texto)

        try:
            response = model.generate_content(prompt)
            raw = response.text.strip()

            # Limpiar posibles bloques de código markdown
            raw = re.sub(r"```(?:json)?", "", raw).strip()

            clasificaciones = json.loads(raw)

            for articulo, clasif in zip(batch, clasificaciones):
                if str(clasif).lower().strip() in ("si", "sí", "yes", "true", "1"):
                    relevantes.append(articulo)

            logger.info(
                f"Gemini batch {batch_idx}/{total_batches}: "
                f"{sum(1 for c in clasificaciones if str(c).lower().strip() in ('si','sí','yes','true','1'))}"
                f"/{len(batch)} relevantes"
            )

        except json.JSONDecodeError:
            logger.warning(f"Gemini respuesta no parseable en batch {batch_idx}; incluyendo batch completo")
            relevantes.extend(batch)
        except Exception as e:
            logger.error(f"Error Gemini batch {batch_idx}: {e}; incluyendo batch completo")
            relevantes.extend(batch)

        # Respetar rate limit del tier gratuito
        if i + BATCH_SIZE < len(articulos):
            time.sleep(2)

    return relevantes, True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logger.info("=" * 65)
    logger.info("  MONITOR NOTICIAS DERECHO MEDIOAMBIENTAL — CHILE")
    logger.info(f"  Inicio: {datetime.now(CHILE_TZ).strftime('%Y-%m-%d %H:%M:%S')} (hora Chile)")
    logger.info("=" * 65)

    # Asegurar que el directorio data/ existe
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Cargar historial de URLs procesadas
    historial = cargar_historial()
    logger.info(f"URLs en historial: {len(historial)}")

    # Importar fuentes
    sys.path.insert(0, str(SCRIPT_DIR))
    from fuentes import FUENTES

    logger.info(f"Fuentes a procesar: {len(FUENTES)}")
    logger.info("-" * 65)

    todos_articulos = []
    fuentes_ok = 0
    fuentes_error = 0

    for fuente in FUENTES:
        nombre = fuente["nombre"]
        try:
            articulos = procesar_fuente(fuente)

            # Filtrar URLs ya vistas
            nuevos = [a for a in articulos if a["url"] not in historial]
            n_skip = len(articulos) - len(nuevos)
            if n_skip > 0:
                logger.info(f"  → {len(nuevos)} nuevos ({n_skip} ya vistos)")
            else:
                logger.info(f"  → {len(nuevos)} nuevos artículos")

            todos_articulos.extend(nuevos)
            fuentes_ok += 1

        except Exception as e:
            logger.error(f"  ERROR procesando {nombre}: {e}")
            fuentes_error += 1

        time.sleep(PAUSA_ENTRE_FUENTES)

    logger.info("-" * 65)
    logger.info(f"Total artículos nuevos candidatos: {len(todos_articulos)}")
    logger.info(f"Fuentes OK: {fuentes_ok} | Con error: {fuentes_error}")

    # Clasificar con Gemini
    if todos_articulos:
        logger.info("\nClasificando con Gemini…")
        noticias_relevantes, gemini_ok = clasificar_con_gemini(todos_articulos)
    else:
        noticias_relevantes = []
        gemini_ok = bool(GEMINI_API_KEY)

    # Ordenar por fecha descendente
    noticias_relevantes.sort(key=lambda x: x.get("fecha", ""), reverse=True)

    # Guardar resultados
    guardar_noticias(noticias_relevantes, gemini_ok)

    # Actualizar historial con todas las URLs encontradas (relevantes o no)
    nuevas_urls = {a["url"] for a in todos_articulos}
    guardar_historial(historial, nuevas_urls)

    logger.info("=" * 65)
    logger.info(f"  COMPLETADO: {len(noticias_relevantes)} noticias relevantes guardadas")
    logger.info(f"  Gemini: {'activo' if gemini_ok else 'no disponible (sin filtro)'}")
    logger.info("=" * 65)


if __name__ == "__main__":
    main()
