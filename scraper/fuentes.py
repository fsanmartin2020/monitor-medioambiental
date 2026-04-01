# -*- coding: utf-8 -*-
"""
Lista de 69 fuentes para el Monitor de Noticias de Derecho Medioambiental Chile.

Cada fuente tiene:
  - nombre:          Nombre visible en la tabla
  - url:             URL base del sitio
  - metodo:          "rss" (preferido) o "scraping"
  - rss_url:         URL principal del feed RSS (si existe)
  - rss_urls:        Lista de URLs RSS alternativas a probar
  - noticias_url:    URL de la sección de noticias (para scraping)
  - categoria:       Categoría de la fuente (para logging)
  - auto_relevante:  True si la fuente es 100% medioambiental (se incluye sin pasar por Gemini)
"""

FUENTES = [

    # =========================================================
    # MEDIOS DE COMUNICACIÓN NACIONALES
    # =========================================================
    {
        "nombre": "Emol",
        "url": "https://www.emol.com",
        "metodo": "rss",
        "rss_url": "https://www.emol.com/rss/Noticias.xml",
        "rss_urls": [
            "https://www.emol.com/rss/Noticias.xml",
            "https://www.emol.com/rss/nacional.xml",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "La Segunda",
        "url": "https://www.lasegunda.com",
        "metodo": "rss",
        "rss_urls": [
            "https://www.lasegunda.com/feed/",
            "https://www.lasegunda.com/rss/",
        ],
        "noticias_url": "https://www.lasegunda.com/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "La Tercera",
        "url": "https://www.latercera.com",
        "metodo": "rss",
        "rss_url": "https://www.latercera.com/feed/",
        "rss_urls": [
            "https://www.latercera.com/feed/",
            "https://www.latercera.com/rss/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "La Nación",
        "url": "https://www.lanacion.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.lanacion.cl/feed/",
            "https://www.lanacion.cl/rss/",
        ],
        "noticias_url": "https://www.lanacion.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "El Mostrador",
        "url": "https://www.elmostrador.cl",
        "metodo": "rss",
        "rss_url": "https://www.elmostrador.cl/feed/",
        "rss_urls": [
            "https://www.elmostrador.cl/feed/",
            "https://www.elmostrador.cl/noticias/feed/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "BioBioChile",
        "url": "https://www.biobiochile.cl",
        "metodo": "rss",
        "rss_url": "https://www.biobiochile.cl/lista/categories/nacional.rss",
        "rss_urls": [
            "https://www.biobiochile.cl/lista/categories/nacional.rss",
            "https://www.biobiochile.cl/feed/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "Cooperativa",
        "url": "https://www.cooperativa.cl",
        "metodo": "rss",
        "rss_url": "https://www.cooperativa.cl/noticias/rss/site/rss.xml",
        "rss_urls": [
            "https://www.cooperativa.cl/noticias/rss/site/rss.xml",
            "https://www.cooperativa.cl/feed/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "El Dínamo",
        "url": "https://www.eldinamo.cl",
        "metodo": "rss",
        "rss_url": "https://www.eldinamo.cl/feed/",
        "rss_urls": [
            "https://www.eldinamo.cl/feed/",
            "https://www.eldinamo.cl/rss/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "Diario Constitucional",
        "url": "http://www.diarioconstitucional.cl",
        "metodo": "rss",
        "rss_urls": [
            "http://www.diarioconstitucional.cl/feed/",
            "https://www.diarioconstitucional.cl/feed/",
        ],
        "noticias_url": "http://www.diarioconstitucional.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "Diario Financiero",
        "url": "https://www.df.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.df.cl/feed/",
            "https://www.df.cl/rss/",
            "https://www.df.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.df.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "Pulso",
        "url": "https://www.pulso.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.pulso.cl/feed/",
            "https://www.pulso.cl/rss/",
        ],
        "noticias_url": "https://www.pulso.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "El Mercurio Legal",
        "url": "https://www.elmercurio.com/legal",
        "metodo": "scraping",
        "noticias_url": "https://www.elmercurio.com/legal/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "El Ciudadano",
        "url": "https://www.elciudadano.cl",
        "metodo": "rss",
        "rss_url": "https://www.elciudadano.cl/feed/",
        "rss_urls": [
            "https://www.elciudadano.cl/feed/",
            "https://www.elciudadano.cl/rss/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "CIPER Chile",
        "url": "https://www.ciperchile.cl",
        "metodo": "rss",
        "rss_url": "https://ciperchile.cl/feed/",
        "rss_urls": [
            "https://ciperchile.cl/feed/",
            "https://www.ciperchile.cl/feed/",
        ],
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "Interferencia",
        "url": "https://interferencia.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://interferencia.cl/feed/",
            "https://interferencia.cl/rss/",
        ],
        "noticias_url": "https://interferencia.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "El Nortero",
        "url": "https://www.elnortero.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.elnortero.cl/feed/",
            "https://www.elnortero.cl/rss/",
        ],
        "noticias_url": "https://www.elnortero.cl/",
        "categoria": "Medio Nacional",
    },
    {
        "nombre": "ADN Prensa",
        "url": "https://www.adprensa.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.adprensa.cl/feed/",
            "https://www.adprensa.cl/rss/",
        ],
        "noticias_url": "https://www.adprensa.cl/",
        "categoria": "Medio Nacional",
    },

    # =========================================================
    # MEDIOS MINERÍA E INDUSTRIA
    # =========================================================
    {
        "nombre": "Minería Chilena (MCH)",
        "url": "https://www.mch.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.mch.cl/feed/",
            "https://www.mch.cl/rss/",
        ],
        "noticias_url": "https://www.mch.cl/",
        "categoria": "Minería",
    },
    {
        "nombre": "Reporte Minero",
        "url": "http://www.reporteminero.cl",
        "metodo": "rss",
        "rss_urls": [
            "http://www.reporteminero.cl/feed/",
            "https://www.reporteminero.cl/feed/",
        ],
        "noticias_url": "http://www.reporteminero.cl/",
        "categoria": "Minería",
    },
    {
        "nombre": "Revista Electricidad e Industria",
        "url": "https://www.revistaei.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.revistaei.cl/feed/",
            "https://www.revistaei.cl/rss/",
        ],
        "noticias_url": "https://www.revistaei.cl/",
        "categoria": "Energía/Industria",
    },
    {
        "nombre": "SONAMI",
        "url": "https://www.sonami.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.sonami.cl/v2/sala-de-prensa/noticias/",
        "categoria": "Minería",
    },
    {
        "nombre": "Portal Minero",
        "url": "http://www.portalminero.com",
        "metodo": "rss",
        "rss_urls": [
            "http://www.portalminero.com/feed/",
            "https://www.portalminero.com/feed/",
        ],
        "noticias_url": "http://www.portalminero.com/",
        "categoria": "Minería",
    },
    {
        "nombre": "Exploraciones Mineras",
        "url": "https://exploracionesmineras.cl",
        "metodo": "scraping",
        "noticias_url": "https://exploracionesmineras.cl/noticias",
        "categoria": "Minería",
    },
    {
        "nombre": "ACADES",
        "url": "https://www.acades.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.acades.cl/feed/",
            "https://www.acades.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.acades.cl/",
        "categoria": "Minería",
    },
    {
        "nombre": "REDIMIN",
        "url": "https://www.redimin.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.redimin.cl/feed/",
            "https://www.redimin.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.redimin.cl/",
        "categoria": "Minería",
    },
    {
        "nombre": "Nueva Minería",
        "url": "http://www.nuevamineria.com",
        "metodo": "rss",
        "rss_urls": [
            "http://www.nuevamineria.com/revista/feed/",
            "https://www.nuevamineria.com/feed/",
        ],
        "noticias_url": "http://www.nuevamineria.com/revista/",
        "categoria": "Minería",
    },

    # =========================================================
    # MEDIOS Y ORGANIZACIONES MEDIOAMBIENTALES
    # =========================================================
    {
        "nombre": "País Circular",
        "url": "https://www.paiscircular.cl",
        "metodo": "rss",
        "rss_url": "https://www.paiscircular.cl/feed/",
        "rss_urls": [
            "https://www.paiscircular.cl/feed/",
            "https://www.paiscircular.cl/rss/",
        ],
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "Industria y Medioambiente",
        "url": "https://www.induambiente.com",
        "metodo": "rss",
        "rss_urls": [
            "https://www.induambiente.com/feed/",
            "https://www.induambiente.com/rss/",
        ],
        "noticias_url": "https://www.induambiente.com/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "Chile Desarrollo Sustentable",
        "url": "http://www.chiledesarrollosustentable.cl",
        "metodo": "rss",
        "rss_urls": [
            "http://www.chiledesarrollosustentable.cl/feed/",
            "https://www.chiledesarrollosustentable.cl/feed/",
        ],
        "noticias_url": "http://www.chiledesarrollosustentable.cl/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "Codex Verde",
        "url": "https://www.codexverde.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.codexverde.cl/feed/",
            "https://www.codexverde.cl/rss/",
        ],
        "noticias_url": "https://www.codexverde.cl/",
        "categoria": "Medioambiente/Derecho",
        "auto_relevante": True,
    },
    {
        "nombre": "CR2 - Centro de Ciencia del Clima",
        "url": "http://www.cr2.cl",
        "metodo": "rss",
        "rss_urls": [
            "http://www.cr2.cl/feed/",
            "https://www.cr2.cl/feed/",
        ],
        "noticias_url": "http://www.cr2.cl/noticias/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "EFE Verde",
        "url": "https://www.efeverde.com",
        "metodo": "rss",
        "rss_url": "https://www.efeverde.com/feed/",
        "rss_urls": [
            "https://www.efeverde.com/feed/",
            "https://www.efeverde.com/rss/",
        ],
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "OLCA",
        "url": "https://www.olca.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.olca.cl/feed/",
            "https://www.olca.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.olca.cl/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "Terram",
        "url": "https://www.terram.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.terram.cl/feed/",
            "https://www.terram.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.terram.cl/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "FIMA",
        "url": "https://www.fima.cl",
        "metodo": "rss",
        "rss_urls": [
            "https://www.fima.cl/feed/",
            "https://www.fima.cl/noticias/feed/",
        ],
        "noticias_url": "https://www.fima.cl/",
        "categoria": "Derecho Ambiental",
        "auto_relevante": True,
    },
    {
        "nombre": "Chile Sustentable",
        "url": "https://www.chilesustentable.net",
        "metodo": "rss",
        "rss_urls": [
            "https://www.chilesustentable.net/feed/",
            "https://chilesustentable.net/feed/",
        ],
        "noticias_url": "https://www.chilesustentable.net/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "DACC - UdeC",
        "url": "http://dacc.udec.cl",
        "metodo": "scraping",
        "noticias_url": "http://dacc.udec.cl/noticias/",
        "categoria": "Medioambiente",
        "auto_relevante": True,
    },
    {
        "nombre": "Fundación Relaves",
        "url": "https://fundacionrelaves.org",
        "metodo": "rss",
        "rss_urls": [
            "https://fundacionrelaves.org/blog/feed/",
            "https://fundacionrelaves.org/feed/",
        ],
        "noticias_url": "https://fundacionrelaves.org/blog/",
        "categoria": "Medioambiente/Minería",
        "auto_relevante": True,
    },

    # =========================================================
    # PODER JUDICIAL Y TRIBUNALES
    # =========================================================
    {
        "nombre": "Poder Judicial (PJUD)",
        "url": "https://www.pjud.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.pjud.cl/prensa-y-comunicaciones/noticias-del-poder-judicial",
        "categoria": "Judicial",
    },
    {
        "nombre": "1er Tribunal Ambiental",
        "url": "https://www.1ta.cl",
        "metodo": "rss",
        "rss_url": "https://www.1ta.cl/feed/",
        "rss_urls": [
            "https://www.1ta.cl/feed/",
        ],
        "noticias_url": "https://www.1ta.cl/noticias/",
        "categoria": "Judicial",
        "auto_relevante": True,
    },
    {
        "nombre": "2do Tribunal Ambiental",
        "url": "https://www.tribunalambiental.cl",
        "metodo": "rss",
        "rss_url": "https://www.tribunalambiental.cl/feed/",
        "rss_urls": [
            "https://www.tribunalambiental.cl/feed/",
        ],
        "noticias_url": "https://www.tribunalambiental.cl/noticias/",
        "categoria": "Judicial",
        "auto_relevante": True,
    },
    {
        "nombre": "3er Tribunal Ambiental",
        "url": "https://3ta.cl",
        "metodo": "rss",
        "rss_url": "https://3ta.cl/feed/",
        "rss_urls": [
            "https://3ta.cl/feed/",
        ],
        "noticias_url": "https://3ta.cl/noticias/",
        "categoria": "Judicial",
        "auto_relevante": True,
    },

    # =========================================================
    # CONGRESO NACIONAL
    # =========================================================
    {
        "nombre": "Cámara de Diputados",
        "url": "https://www.camara.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.camara.cl/prensa/prensa_cms.aspx",
        "categoria": "Congreso",
    },
    {
        "nombre": "Senado",
        "url": "https://www.senado.cl",
        "metodo": "sitemap",
        "sitemap_url": "https://www.senado.cl/sitemap.xml",
        "noticias_url": "https://www.senado.cl/noticias/",
        "categoria": "Congreso",
    },

    # =========================================================
    # MINISTERIOS Y ORGANISMOS DE GOBIERNO
    # =========================================================
    {
        "nombre": "CONADI",
        "url": "http://www.conadi.gob.cl",
        "metodo": "scraping",
        "noticias_url": "http://www.conadi.gob.cl/noticias",
        "categoria": "Gobierno",
    },
    {
        "nombre": "Ministerio Desarrollo Social",
        "url": "http://www.ministeriodesarrollosocial.gob.cl",
        "metodo": "scraping",
        "noticias_url": "http://www.ministeriodesarrollosocial.gob.cl/noticias",
        "categoria": "Gobierno",
    },
    {
        "nombre": "SII - Normativa",
        "url": "https://www.sii.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.sii.cl/normativa_legislacion/",
        "categoria": "Gobierno",
    },
    {
        "nombre": "Bienes Nacionales",
        "url": "http://www.bienesnacionales.cl",
        "metodo": "rss",
        "rss_url": "http://www.bienesnacionales.cl/feed/",
        "rss_urls": [
            "http://www.bienesnacionales.cl/feed/",
            "https://www.bienesnacionales.cl/feed/",
        ],
        "noticias_url": "http://www.bienesnacionales.cl/?cat=7",
        "categoria": "Gobierno",
    },
    {
        "nombre": "MINSAL",
        "url": "https://www.minsal.cl",
        "metodo": "rss",
        "rss_url": "https://www.minsal.cl/feed/",
        "rss_urls": [
            "https://www.minsal.cl/feed/",
        ],
        "noticias_url": "https://www.minsal.cl/noticias/",
        "categoria": "Gobierno",
    },
    {
        "nombre": "Ministerio de Transportes",
        "url": "https://www.mtt.gob.cl",
        "metodo": "rss",
        "rss_url": "https://www.mtt.gob.cl/feed/",
        "rss_urls": [
            "https://www.mtt.gob.cl/feed/",
        ],
        "noticias_url": "https://www.mtt.gob.cl/noticias/",
        "categoria": "Gobierno",
    },
    {
        "nombre": "SISS",
        "url": "http://www.siss.gob.cl",
        "metodo": "scraping",
        "noticias_url": "http://www.siss.gob.cl/586/w3-channel.html",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "DIRECTEMAR",
        "url": "https://www.directemar.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.directemar.cl/directemar/sala-de-prensa/noticias",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "SERNAPESCA",
        "url": "https://www.sernapesca.cl",
        "metodo": "sitemap",
        "sitemap_url": "https://www.sernapesca.cl/sitemap.xml",
        "noticias_url": "https://www.sernapesca.cl/noticias/",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "Subsecretaría de Pesca",
        "url": "https://www.subpesca.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.subpesca.cl/portal/sitio/",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "SAG",
        "url": "https://www.sag.gob.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.sag.gob.cl/ambito/noticias",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "CONAF",
        "url": "https://www.conaf.cl",
        "metodo": "rss",
        "rss_url": "https://www.conaf.cl/feed/",
        "rss_urls": [
            "https://www.conaf.cl/feed/",
        ],
        "noticias_url": "https://www.conaf.cl/noticias/",
        "categoria": "Gobierno",
        "auto_relevante": True,
    },
    {
        "nombre": "Ministerio de Energía",
        "url": "http://www.energia.gob.cl",
        "metodo": "scraping",
        "noticias_url": "http://www.energia.gob.cl/noticias",
        "categoria": "Gobierno",
    },
    {
        "nombre": "CNE",
        "url": "http://www.cne.cl",
        "metodo": "rss",
        "rss_url": "http://www.cne.cl/feed/",
        "rss_urls": [
            "http://www.cne.cl/feed/",
            "https://www.cne.cl/feed/",
        ],
        "noticias_url": "http://www.cne.cl/noticias/",
        "categoria": "Gobierno",
    },
    {
        "nombre": "Ministerio de Economía",
        "url": "http://www.economia.gob.cl",
        "metodo": "rss",
        "rss_url": "http://www.economia.gob.cl/feed/",
        "rss_urls": [
            "http://www.economia.gob.cl/feed/",
            "https://www.economia.gob.cl/feed/",
        ],
        "noticias_url": "http://www.economia.gob.cl/noticias",
        "categoria": "Gobierno",
    },
    {
        "nombre": "SEA",
        "url": "https://www.sea.gob.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.sea.gob.cl/noticias",
        "categoria": "Medioambiente/Regulación",
        "auto_relevante": True,
    },
    {
        "nombre": "SMA",
        "url": "https://portal.sma.gob.cl",
        "metodo": "rss",
        "rss_url": "https://portal.sma.gob.cl/index.php/feed/",
        "categoria": "Medioambiente/Regulación",
        "auto_relevante": True,
    },
    {
        "nombre": "Ministerio de Minería",
        "url": "https://www.minmineria.cl",
        "metodo": "scraping",
        "noticias_url": "https://www.minmineria.cl/noticias/",
        "categoria": "Gobierno",
    },
    {
        "nombre": "COCHILCO",
        "url": "http://www.cochilco.cl",
        "metodo": "scraping",
        "noticias_url": "http://www.cochilco.cl/noticias/",
        "categoria": "Minería",
    },
    {
        "nombre": "Comisión Minera",
        "url": "https://www.comisionminera.cl",
        "metodo": "rss",
        "rss_url": "https://www.comisionminera.cl/feed/",
        "rss_urls": [
            "https://www.comisionminera.cl/feed/",
        ],
        "noticias_url": "https://www.comisionminera.cl/noticias/",
        "categoria": "Minería",
    },
    {
        "nombre": "SERNAGEOMIN",
        "url": "https://www.sernageomin.cl",
        "metodo": "rss",
        "rss_url": "https://www.sernageomin.cl/feed/",
        "rss_urls": [
            "https://www.sernageomin.cl/feed/",
        ],
        "sitemap_url": "https://www.sernageomin.cl/sitemap.xml",
        "noticias_url": "https://www.sernageomin.cl/noticias/",
        "categoria": "Minería",
        "auto_relevante": True,
    },
    {
        "nombre": "DGA - MOP",
        "url": "https://dga.mop.gob.cl",
        "metodo": "rss",
        "rss_url": "https://dga.mop.gob.cl/feed/",
        "rss_urls": [
            "https://dga.mop.gob.cl/feed/",
        ],
        "noticias_url": "https://dga.mop.gob.cl/noticias/",
        "categoria": "Agua",
        "auto_relevante": True,
    },
    {
        "nombre": "Ministerio del Medio Ambiente",
        "url": "https://mma.gob.cl",
        "metodo": "rss",
        "rss_url": "https://mma.gob.cl/feed/",
        "rss_urls": [
            "https://mma.gob.cl/feed/",
        ],
        "noticias_url": "https://mma.gob.cl/noticias/",
        "categoria": "Medioambiente/Regulación",
        "auto_relevante": True,
    },
    {
        "nombre": "Acuerdo de Escazú - MMA",
        "url": "https://escazu.mma.gob.cl",
        "metodo": "scraping",
        "noticias_url": "https://escazu.mma.gob.cl/",
        "categoria": "Derecho Ambiental Internacional",
        "auto_relevante": True,
    },
    {
        "nombre": "RETC",
        "url": "https://retc.mma.gob.cl",
        "metodo": "rss",
        "rss_url": "https://retc.mma.gob.cl/feed/",
        "rss_urls": [
            "https://retc.mma.gob.cl/feed/",
        ],
        "noticias_url": "https://retc.mma.gob.cl/",
        "categoria": "Medioambiente/Regulación",
        "auto_relevante": True,
    },
]
