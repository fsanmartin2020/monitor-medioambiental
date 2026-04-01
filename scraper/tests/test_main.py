"""
Tests de regresión para scraper/main.py
========================================
Cubre: parse_fecha, es_reciente, normalizar_url,
       intentar_rss (fallback), _filtrar_sin_fecha, detectar_alertas,
       _prefiltro_keywords.

Ejecutar desde la raíz del proyecto:
    pytest scraper/tests/ -v
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

# Agregar scraper/ al path para importar main sin instalación
sys.path.insert(0, str(Path(__file__).parent.parent))
import main  # noqa: E402  (importación después de sys.path)


# ---------------------------------------------------------------------------
# Helpers compartidos
# ---------------------------------------------------------------------------

def _articulo(titular="Titular de prueba", fecha_confiable=True, url="https://ejemplo.cl/nota"):
    """Crea un artículo mínimo válido para los tests."""
    return {
        "fuente": "Fuente Test",
        "titular": titular,
        "url": url,
        "fecha": "2026-01-01",
        "fecha_confiable": fecha_confiable,
        "metodo_extraccion": "rss",
    }


# ===========================================================================
# parse_fecha
# ===========================================================================

class TestParseFecha:
    """Formatos de fecha que el scraper debe ser capaz de interpretar."""

    def test_iso_con_tz_negativa(self):
        """ISO 8601 con offset explícito -03:00."""
        dt = main.parse_fecha("2024-03-15T10:30:00-03:00")
        assert dt is not None
        assert dt.tzinfo is not None
        assert dt.year == 2024 and dt.month == 3 and dt.day == 15

    def test_iso_con_z_utc(self):
        """ISO 8601 con sufijo Z → UTC."""
        dt = main.parse_fecha("2024-03-15T10:30:00Z")
        assert dt is not None
        assert dt.tzinfo is not None
        assert dt.utcoffset() == timedelta(0)

    def test_formato_espanol_basico(self):
        """'15 de marzo de 2024' → fecha con tz Chile."""
        dt = main.parse_fecha("15 de marzo de 2024")
        assert dt is not None
        assert dt.year == 2024
        assert dt.month == 3
        assert dt.day == 15
        assert dt.tzinfo is not None

    def test_formato_espanol_mes_enero(self):
        dt = main.parse_fecha("5 de enero de 2025")
        assert dt is not None
        assert dt.month == 1
        assert dt.day == 5

    def test_formato_espanol_diciembre(self):
        dt = main.parse_fecha("31 de diciembre de 2023")
        assert dt is not None
        assert dt.month == 12
        assert dt.day == 31

    def test_iso_sin_tz_asume_chile(self):
        """Fecha sin timezone → debe asumir zona horaria Chile."""
        dt = main.parse_fecha("2024-03-15")
        assert dt is not None
        assert dt.tzinfo is not None  # debe tener tz aunque no venga en el string

    def test_iso_datetime_sin_tz(self):
        """Datetime ISO sin tz → asume Chile."""
        dt = main.parse_fecha("2024-06-20T15:00:00")
        assert dt is not None
        assert dt.tzinfo is not None
        assert dt.hour == 15

    def test_string_vacio_retorna_none(self):
        assert main.parse_fecha("") is None

    def test_none_retorna_none(self):
        assert main.parse_fecha(None) is None

    def test_string_invalido_retorna_none(self):
        assert main.parse_fecha("esto no es una fecha") is None

    def test_rss_fecha_tipica(self):
        """Formato habitual de feeds RSS: 'Fri, 29 Mar 2024 10:00:00 +0000'."""
        dt = main.parse_fecha("Fri, 29 Mar 2024 10:00:00 +0000")
        assert dt is not None
        assert dt.tzinfo is not None
        assert dt.month == 3 and dt.day == 29


# ===========================================================================
# es_reciente
# ===========================================================================

class TestEsReciente:
    """La ventana de 24 horas debe funcionar correctamente en todos los casos."""

    def test_none_retorna_true(self):
        """Sin fecha → incluir para que el pipeline decida después."""
        assert main.es_reciente(None) is True

    def test_hace_1_hora_es_reciente(self):
        fecha = datetime.now(timezone.utc) - timedelta(hours=1)
        assert main.es_reciente(fecha) is True

    def test_hace_23_horas_es_reciente(self):
        fecha = datetime.now(timezone.utc) - timedelta(hours=23)
        assert main.es_reciente(fecha) is True

    def test_hace_25_horas_no_es_reciente(self):
        fecha = datetime.now(timezone.utc) - timedelta(hours=25)
        assert main.es_reciente(fecha) is False

    def test_futuro_es_reciente(self):
        """Fechas futuras (posible desfase de reloj) deben pasar."""
        fecha = datetime.now(timezone.utc) + timedelta(hours=2)
        assert main.es_reciente(fecha) is True

    def test_naive_asume_chile(self):
        """Datetime sin tz → se interpreta como hora Chile → 1h atrás = reciente."""
        chile_tz = ZoneInfo("America/Santiago")
        fecha_naive = datetime.now(chile_tz).replace(tzinfo=None) - timedelta(hours=1)
        assert main.es_reciente(fecha_naive) is True

    def test_naive_antiguo_no_es_reciente(self):
        """Datetime naive muy antiguo → aunque sea Chile, no es reciente."""
        chile_tz = ZoneInfo("America/Santiago")
        fecha_naive = datetime.now(chile_tz).replace(tzinfo=None) - timedelta(hours=30)
        assert main.es_reciente(fecha_naive) is False

    def test_ventana_custom_6h(self):
        """Con ventana de 6h, una noticia de 8h atrás no pasa."""
        fecha = datetime.now(timezone.utc) - timedelta(hours=8)
        assert main.es_reciente(fecha, horas=6) is False
        assert main.es_reciente(fecha, horas=24) is True

    def test_ventana_custom_48h(self):
        fecha = datetime.now(timezone.utc) - timedelta(hours=36)
        assert main.es_reciente(fecha, horas=48) is True
        assert main.es_reciente(fecha, horas=24) is False


# ===========================================================================
# normalizar_url
# ===========================================================================

class TestNormalizarUrl:
    """La canonicalización debe hacer URLs comparables independiente de UTMs y formato."""

    def test_elimina_barra_final(self):
        assert main.normalizar_url("https://ejemplo.cl/noticia/") == "https://ejemplo.cl/noticia"

    def test_preserva_raiz(self):
        """La barra raíz no debe eliminarse."""
        result = main.normalizar_url("https://ejemplo.cl/")
        assert result.startswith("https://ejemplo.cl")

    def test_lowercase_scheme(self):
        assert main.normalizar_url("HTTPS://ejemplo.cl/nota").startswith("https://")

    def test_lowercase_host(self):
        result = main.normalizar_url("https://EMOL.COM/nota")
        assert "emol.com" in result
        assert "EMOL.COM" not in result

    def test_elimina_utm_source(self):
        url = "https://ejemplo.cl/art?utm_source=twitter"
        assert "utm_source" not in main.normalizar_url(url)

    def test_elimina_todos_utm(self):
        url = "https://ejemplo.cl/art?utm_source=tw&utm_medium=social&utm_campaign=test&utm_content=x"
        result = main.normalizar_url(url)
        assert "utm_" not in result
        assert result == "https://ejemplo.cl/art"

    def test_elimina_fbclid(self):
        url = "https://ejemplo.cl/art?fbclid=IwAR123abc"
        assert "fbclid" not in main.normalizar_url(url)

    def test_elimina_gclid(self):
        url = "https://ejemplo.cl/art?gclid=Cj0KCQ"
        assert "gclid" not in main.normalizar_url(url)

    def test_conserva_params_reales(self):
        url = "https://ejemplo.cl/art?id=123&page=2"
        result = main.normalizar_url(url)
        assert "id=123" in result
        assert "page=2" in result

    def test_ordena_params_alfabeticamente(self):
        """Dos URLs con los mismos parámetros en orden distinto deben normalizarse igual."""
        url1 = "https://ejemplo.cl/art?z=1&a=2&m=3"
        url2 = "https://ejemplo.cl/art?m=3&z=1&a=2"
        assert main.normalizar_url(url1) == main.normalizar_url(url2)

    def test_mezcla_utm_y_param_real(self):
        url = "https://ejemplo.cl/art?id=5&utm_source=tw&utm_medium=social"
        result = main.normalizar_url(url)
        assert "id=5" in result
        assert "utm_source" not in result
        assert "utm_medium" not in result

    def test_dedup_misma_url_con_y_sin_utm(self):
        """La misma URL con y sin UTMs debe normalizarse igual → deduplicación correcta."""
        limpia = "https://ejemplo.cl/nota"
        con_utm = "https://ejemplo.cl/nota?utm_source=newsletter&utm_medium=email"
        assert main.normalizar_url(limpia) == main.normalizar_url(con_utm)

    def test_url_invalida_devuelve_original(self):
        url = "esto no es una url"
        assert main.normalizar_url(url) == url


# ===========================================================================
# intentar_rss — fallback
# ===========================================================================

class TestIntentarRss:
    """El fallback RSS → sitemap/scraping debe activarse en los casos correctos."""

    def test_todos_fallan_retorna_none(self):
        """Si todos los feeds lanzan excepción → None para activar fallback."""
        fuente = {"nombre": "Test", "metodo": "rss", "rss_url": "http://test.cl/feed"}
        with patch("main.feedparser.parse", side_effect=Exception("timeout")):
            result = main.intentar_rss(fuente)
        assert result is None

    def test_feed_valido_con_entradas_retorna_lista(self):
        """Feed accesible y con entradas → retorna lista (puede estar vacía)."""
        fuente = {"nombre": "Test", "metodo": "rss", "rss_url": "http://test.cl/feed"}
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = [MagicMock()]  # una entrada → feed no está vacío

        with patch("main.feedparser.parse", return_value=mock_feed):
            with patch("main.fetch_rss", return_value=[]) as mock_fetch:
                result = main.intentar_rss(fuente)

        assert result is not None          # lista (aunque vacía)
        mock_fetch.assert_called_once()    # fetch_rss fue invocado

    def test_feed_vacio_sin_entradas_retorna_none(self):
        """Feed válido pero sin entradas → None para activar fallback a sitemap/scraping."""
        fuente = {"nombre": "Test", "metodo": "rss", "rss_url": "http://test.cl/feed"}
        mock_feed = MagicMock()
        mock_feed.bozo = False
        mock_feed.entries = []  # feed vacío

        with patch("main.feedparser.parse", return_value=mock_feed):
            result = main.intentar_rss(fuente)

        assert result is None  # debe caer al siguiente método

    def test_multiple_rss_urls_prueba_todas(self):
        """Con múltiples RSS URLs, si la primera falla prueba la segunda."""
        fuente = {
            "nombre": "Test",
            "metodo": "rss",
            "rss_urls": ["http://test.cl/feed1", "http://test.cl/feed2"],
        }
        mock_feed_vacio = MagicMock()
        mock_feed_vacio.bozo = False
        mock_feed_vacio.entries = []

        mock_feed_con_entradas = MagicMock()
        mock_feed_con_entradas.bozo = False
        mock_feed_con_entradas.entries = [MagicMock()]

        respuestas = [mock_feed_vacio, mock_feed_con_entradas]

        with patch("main.feedparser.parse", side_effect=respuestas):
            with patch("main.fetch_rss", return_value=[_articulo()]):
                result = main.intentar_rss(fuente)

        assert result is not None

    def test_sin_rss_urls_retorna_none(self):
        """Fuente sin ninguna URL RSS configurada → None inmediato."""
        fuente = {"nombre": "Test", "metodo": "scraping", "noticias_url": "http://test.cl"}
        result = main.intentar_rss(fuente)
        assert result is None


# ===========================================================================
# _filtrar_sin_fecha
# ===========================================================================

class TestFiltrarSinFecha:
    """Filtrado de artículos sin fecha confiable según el tipo de fuente."""

    def test_no_auto_pasa_todos(self):
        """Fuente generalista → todos pasan sin importar fecha_confiable."""
        arts = [_articulo(fecha_confiable=False), _articulo(fecha_confiable=False)]
        result = main._filtrar_sin_fecha(arts, "Test", es_auto=False)
        assert len(result) == 2

    def test_auto_descarta_sin_fecha(self):
        """Fuente auto_relevante → solo pasan los que tienen fecha confiable."""
        arts = [
            _articulo(fecha_confiable=True),
            _articulo(fecha_confiable=False),
            _articulo(fecha_confiable=True),
        ]
        result = main._filtrar_sin_fecha(arts, "Test", es_auto=True)
        assert len(result) == 2
        assert all(a["fecha_confiable"] is True for a in result)

    def test_auto_todos_validos_pasan(self):
        arts = [_articulo(fecha_confiable=True), _articulo(fecha_confiable=True)]
        result = main._filtrar_sin_fecha(arts, "Test", es_auto=True)
        assert len(result) == 2

    def test_auto_todos_sin_fecha_retorna_vacio(self):
        arts = [_articulo(fecha_confiable=False), _articulo(fecha_confiable=False)]
        result = main._filtrar_sin_fecha(arts, "Test", es_auto=True)
        assert len(result) == 0

    def test_lista_vacia_no_falla(self):
        result = main._filtrar_sin_fecha([], "Test", es_auto=True)
        assert result == []

    def test_sin_campo_fecha_confiable_pasa(self):
        """Artículo sin el campo fecha_confiable → se asume True (comportamiento seguro)."""
        art = {"fuente": "T", "titular": "T", "url": "http://x.cl", "fecha": "2024-01-01"}
        result = main._filtrar_sin_fecha([art], "Test", es_auto=True)
        assert len(result) == 1


# ===========================================================================
# detectar_alertas
# ===========================================================================

class TestDetectarAlertas:
    """Detección de keywords de alta urgencia jurídico-ambiental."""

    def test_sma_detectado(self):
        noticias = [_articulo("SMA sanciona empresa por daño al humedal")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1
        assert "SMA" in alertas[0]["keywords_detectadas"]

    def test_tribunal_ambiental_detectado(self):
        noticias = [_articulo("Tribunal Ambiental rechaza EIA de proyecto minero")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1
        kws = alertas[0]["keywords_detectadas"]
        assert "Tribunal Ambiental" in kws or "EIA" in kws

    def test_sin_keywords_no_es_alerta(self):
        noticias = [_articulo("Selección chilena gana partido amistoso en Europa")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 0

    def test_multiples_keywords_en_mismo_titular(self):
        noticias = [_articulo("SMA impone multa ambiental a empresa con RCA vencida")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1
        assert len(alertas[0]["keywords_detectadas"]) >= 2

    def test_case_insensitive(self):
        """Las keywords deben detectarse sin importar mayúsculas/minúsculas."""
        noticias = [_articulo("sma sanciona empresa por derrame en río")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1

    def test_lista_mixta(self):
        noticias = [
            _articulo("SMA inicia sumario ambiental contra minera"),
            _articulo("Precio del dólar sube por tensiones comerciales"),
            _articulo("Corte Suprema falla contra proyecto en zona de sacrificio"),
            _articulo("Selección femenina clasifica al mundial"),
        ]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 2

    def test_escazu_detectado(self):
        noticias = [_articulo("Chile ratifica compromisos del Acuerdo de Escazú")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1

    def test_seia_detectado(self):
        noticias = [_articulo("Proyecto ingresa al SEIA para evaluación ambiental")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1

    def test_zona_sacrificio_detectada(self):
        noticias = [_articulo("Comunidades en zona de sacrificio exigen reparación")]
        alertas = main.detectar_alertas(noticias)
        assert len(alertas) == 1

    def test_lista_vacia_retorna_vacia(self):
        assert main.detectar_alertas([]) == []

    def test_keywords_detectadas_se_agrega_al_articulo(self):
        """El artículo alerta debe tener el campo keywords_detectadas."""
        noticias = [_articulo("SMA aplica sanción ambiental histórica")]
        alertas = main.detectar_alertas(noticias)
        assert "keywords_detectadas" in alertas[0]
        assert isinstance(alertas[0]["keywords_detectadas"], list)


# ===========================================================================
# _prefiltro_keywords
# ===========================================================================

class TestPrefiltroKeywords:
    """El pre-filtro debe clasificar sin ambigüedad los casos claros."""

    def _art_con_extracto(self, titular, extracto=""):
        a = _articulo(titular)
        a["extracto"] = extracto
        return a

    def test_auto_si_por_titular(self):
        arts = [self._art_con_extracto("SEIA aprueba proyecto hidroeléctrico")]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(auto_si) == 1
        assert len(auto_no) == 0
        assert len(ambiguos) == 0

    def test_auto_si_por_extracto(self):
        """Debe detectar en extracto aunque el titular sea ambiguo."""
        arts = [self._art_con_extracto(
            "Codelco anuncia nuevo proyecto en el norte",
            "La empresa presentó el EIA ante el Tribunal Ambiental esta semana."
        )]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(auto_si) == 1

    def test_auto_no_por_titular(self):
        arts = [self._art_con_extracto("Chile vence a Argentina en Copa Libertadores")]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(auto_no) == 1
        assert len(auto_si) == 0
        assert len(ambiguos) == 0

    def test_ambiguo_va_a_gemini(self):
        """Titular sin keywords claras → debe ir a Gemini."""
        arts = [self._art_con_extracto("Gobierno anuncia nueva política energética")]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(ambiguos) == 1

    def test_lista_mixta(self):
        arts = [
            self._art_con_extracto("SMA multa empresa por vertido"),           # auto_si
            self._art_con_extracto("Champions League: Real Madrid clasifica"),  # auto_no
            self._art_con_extracto("Economía chilena creció un 2% en marzo"),   # ambiguo
            self._art_con_extracto("Tribunal Ambiental falla en caso minero"),  # auto_si
        ]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(auto_si) == 2
        assert len(auto_no) == 1
        assert len(ambiguos) == 1

    def test_lista_vacia(self):
        auto_si, auto_no, ambiguos = main._prefiltro_keywords([])
        assert auto_si == [] and auto_no == [] and ambiguos == []

    def test_auto_si_tiene_prioridad_sobre_auto_no(self):
        """Si un titular tiene keywords de ambas listas, auto_si gana."""
        arts = [self._art_con_extracto(
            "Dow Jones sube pero SEIA rechaza proyecto minero"
        )]
        auto_si, auto_no, ambiguos = main._prefiltro_keywords(arts)
        assert len(auto_si) == 1  # SEIA gana sobre Dow Jones
