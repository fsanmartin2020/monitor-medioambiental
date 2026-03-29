# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chilean environmental law news monitor. A Python scraper runs daily via GitHub Actions, fetches articles from 69 configured sources (RSS, sitemap, HTML scraping), classifies them with Google Gemini AI for relevance to environmental law, and publishes results as a static JSON-powered web page hosted on Vercel.

## Commands

```bash
# Run the scraper (requires GEMINI_API_KEY env var for AI filtering; works without it but shows all unfiltered)
GEMINI_API_KEY=your_key python scraper/main.py

# Run source diagnostics (no API key needed — tests all 69 sources for connectivity)
python scraper/diagnostico.py

# Install dependencies
pip install -r scraper/requirements.txt
```

There are no tests, linter, or build steps. The frontend is a single `index.html` with inline CSS/JS — no build tooling.

## Architecture

**Scraper pipeline** (`scraper/main.py`):
1. Loads source definitions from `scraper/fuentes.py` (list of dicts with name, URL, method, RSS/sitemap URLs)
2. For each source, tries extraction in order: RSS → sitemap → generic HTML scraping (JSON-LD → `<article>` tags → generic links)
3. Filters by recency (24-hour window) and deduplicates against `data/historial.json`
4. Sends article titles to Gemini in batches of 15 for relevance classification (si/no)
5. Writes results to `data/noticias.json` and updates `data/historial.json`

**Frontend** (`index.html`): Single-page app that fetches `data/noticias.json` at load time. Client-side filtering, sorting, and search. No framework.

**CI/CD** (`.github/workflows/actualizar.yml`): Runs daily at 11:00 UTC (8:00 AM Chile). Executes the scraper, commits updated JSON files, and pushes. Vercel auto-deploys on push.

## Key Design Decisions

- **Three-tier scraping fallback**: RSS is preferred; if it fails, sitemap is tried; then generic HTML scraping with progressively less-structured extraction (JSON-LD → article containers → link text)
- **Conservative AI classification**: When Gemini fails for a batch after retries, the batch is discarded (fewer false positives preferred over missing articles)
- **Historial cap**: `historial.json` is capped at 8,000 URLs to prevent unbounded growth
- **All data is static JSON**: No database, no backend server. The scraper writes files, git commits them, and the frontend reads them directly

## Adding/Modifying Sources

Edit `scraper/fuentes.py`. Each source dict requires `nombre`, `url`, `metodo` ("rss", "sitemap", or "scraping"), and the relevant URL fields (`rss_url`/`rss_urls`, `sitemap_url`, `noticias_url`). The `categoria` field is for logging only.

## Language

The codebase, comments, variable names, and user-facing text are in **Spanish**. Follow this convention.
