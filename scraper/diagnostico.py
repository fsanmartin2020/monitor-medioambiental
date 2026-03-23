#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico de fuentes — Monitor Medioambiental Chile
=====================================================
Prueba cada fuente configurada y reporta si está devolviendo artículos.

Uso:
    python scraper/diagnostico.py

No requiere GEMINI_API_KEY. Solo prueba el scraping/RSS.
"""

import sys
import time
from pathlib import Path

# Agregar el directorio scraper al path para importar fuentes y main
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

import logging
logging.disable(logging.CRITICAL)  # silenciar logs del main durante diagnóstico

from fuentes import FUENTES
from main import procesar_fuente

PAUSA = 0.5  # segundos entre fuentes para no saturar

VERDE  = "\033[92m"
AMARILLO = "\033[93m"
ROJO   = "\033[91m"
RESET  = "\033[0m"
NEGRITA = "\033[1m"


def color_estado(n: int, error: bool) -> str:
    if error:
        return f"{ROJO}ERROR{RESET}"
    if n == 0:
        return f"{AMARILLO}VACÍO{RESET}"
    return f"{VERDE}OK ({n}){RESET}"


def main():
    print(f"\n{NEGRITA}{'='*65}{RESET}")
    print(f"{NEGRITA}  DIAGNÓSTICO DE FUENTES — MONITOR MEDIOAMBIENTAL CHILE{RESET}")
    print(f"{NEGRITA}{'='*65}{RESET}")
    print(f"  Probando {len(FUENTES)} fuentes...\n")

    resultados = []

    for fuente in FUENTES:
        nombre    = fuente["nombre"]
        metodo    = fuente.get("metodo", "rss")
        categoria = fuente.get("categoria", "")

        error = False
        articulos = []

        try:
            articulos = procesar_fuente(fuente)
        except Exception as e:
            error = True
            articulos = []

        n = len(articulos)
        estado = color_estado(n, error)

        print(f"  [{metodo.upper():7s}]  {nombre:<40s}  {estado}")

        resultados.append({
            "nombre": nombre,
            "metodo": metodo,
            "categoria": categoria,
            "n": n,
            "error": error,
        })

        time.sleep(PAUSA)

    # ---- Resumen ----
    ok      = [r for r in resultados if not r["error"] and r["n"] > 0]
    vacios  = [r for r in resultados if not r["error"] and r["n"] == 0]
    errores = [r for r in resultados if r["error"]]

    print(f"\n{NEGRITA}{'='*65}{RESET}")
    print(f"{NEGRITA}  RESUMEN{RESET}")
    print(f"{NEGRITA}{'='*65}{RESET}")
    print(f"  {VERDE}Con artículos:{RESET}  {len(ok)}/{len(FUENTES)}")
    print(f"  {AMARILLO}Vacías (0 art):{RESET} {len(vacios)}/{len(FUENTES)}")
    print(f"  {ROJO}Con error:{RESET}      {len(errores)}/{len(FUENTES)}")

    if vacios:
        print(f"\n{NEGRITA}  Fuentes sin artículos hoy (puede ser normal si no publicaron):{RESET}")
        for r in vacios:
            print(f"    - {r['nombre']} [{r['metodo']}] ({r['categoria']})")

    if errores:
        print(f"\n{NEGRITA}  Fuentes con error (revisar URL o acceso):{RESET}")
        for r in errores:
            print(f"    - {r['nombre']} [{r['metodo']}] ({r['categoria']})")

    print(f"\n{NEGRITA}  NOTA:{RESET} 'VACÍO' en un día sin publicaciones es normal.")
    print( "  'VACÍO' o 'ERROR' repetidos varios días seguidos indica un problema.\n")


if __name__ == "__main__":
    main()
