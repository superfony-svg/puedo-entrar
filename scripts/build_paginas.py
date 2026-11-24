#!/usr/bin/env python3
"""Genera una página por ciudad (para Google), el mapa del sitio y la lista de
ciudades de la portada, a partir de web/data/zonas.json.

Uso: python scripts/build_paginas.py web
"""
import html
import json
import os
import re
import sys
import unicodedata
from datetime import date

from guias import GUIAS

BASE = os.environ.get("BASE_URL", "https://superfony-svg.github.io/puedo-entrar/")
NOMBRES = {"0": "Cero emisiones", "E": "ECO", "C": "C (verde)", "B": "B (amarilla)", "N": "Sin etiqueta"}
TODAS = ["0", "E", "C", "B", "N"]

CSS = """
:root{--bg:#f3f5f4;--surface:#fff;--fg:#17211d;--muted:#5b6862;--line:#d7dedb;--accent:#1f6f5c;--ok:#1d8a4e;--no:#c0392b;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#101614;--surface:#18201d;--fg:#e6eeea;--muted:#9aa8a1;--line:#2b3733;--accent:#5cc3a6;--ok:#4fd08a;--no:#ff7a6b;color-scheme:dark}}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--fg);font:16px/1.55 Inter,system-ui,sans-serif}
.wrap{max-width:640px;margin:0 auto;padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:flex;flex-direction:column;gap:18px}
h1{font:700 clamp(1.6rem,6vw,2.2rem)/1.15 "Space Grotesk",system-ui,sans-serif;margin:0;text-wrap:balance}
h2{font:700 1.15rem "Space Grotesk",system-ui,sans-serif;margin:0}
a{color:var(--accent)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px;display:flex;flex-direction:column;gap:10px}
form{display:flex;gap:8px;flex-wrap:wrap}
.plate{flex:1 1 200px;min-width:0;display:flex;border:2px solid var(--fg);border-radius:8px;overflow:hidden;background:#fff}
.plate span{background:#1f4fb8;color:#fff;font-size:.7rem;font-weight:700;display:flex;align-items:flex-end;padding:6px 7px}
.plate input{flex:1;min-width:0;border:0;font:700 1.5rem/1 "Space Grotesk",system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;padding:10px 12px;color:#111;background:#fff}
button{font:inherit;font-weight:600;border:0;border-radius:10px;padding:12px 18px;background:var(--accent);color:var(--bg);cursor:pointer}
dl{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0}dt{color:var(--muted);font-size:.85rem}dd{margin:0;min-width:0}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{padding:3px 10px;border-radius:999px;font-size:.9rem;font-weight:600;border:1.5px solid}
.chip.ok{color:var(--ok);border-color:var(--ok)}.chip.no{color:var(--no);border-color:var(--no)}
.muted{color:var(--muted);font-size:.88rem;margin:0}
footer{font-size:.8rem;color:var(--muted)}
ul,ol{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:6px}p{margin:0}
details{border-top:1px solid var(--line);padding-top:10px}summary{font-weight:600;cursor:pointer}details p{margin-top:6px}
.guias{display:flex;flex-wrap:wrap;gap:6px 14px}
"""


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fecha(iso):
    return "/".join(reversed(iso.split("-"))) if iso else ""


def horario(z):
    if not z.get("horario"):
        return "Consulta el horario en la web del ayuntamiento."
    out = []
    for h in z["horario"]:
        a = "24:00" if h.get("a") == "23:59" else h.get("a", "")
        out.append(h["dias"] + (f" de {h['de']} a {a}" if h.get("de") else ""))
    return " · ".join(out)


def e(s):
    return html.escape(s or "", quote=True)


def zona_html(z, ciudad):
    rows = []
    if z.get("zona"):
        rows.append(("Zona", e(z["zona"])))
    if z.get("aviso"):
        rows.append(("Aviso", f'<strong>{e(z["aviso"])}</strong>' + (f' <a href="{e(z["aviso_fuente"])}" target="_blank" rel="noopener">Fuente</a>' if z.get("aviso_fuente") else "")))
    elif z.get("estado") and z["estado"] != "active":
        rows.append(("Estado", "Aún no está activa"))
    elif z.get("desde") and z["desde"] > date.today().isoformat():
        rows.append(("Estado", f"Se aplicará desde el {fecha(z['desde'])}"))
    if z.get("permitidas"):
        chips = "".join(
            f'<span class="chip {"ok" if k in z["permitidas"] else "no"}">{"✓" if k in z["permitidas"] else "✗"} {NOMBRES[k]}</span>'
            for k in TODAS)
        rows.append(("Etiquetas", f'<div class="chips">{chips}</div>'))
    else:
        rows.append(("Etiquetas", "Los datos publicados por la DGT no son claros: consulta la web del ayuntamiento."))
    if z.get("solo_episodios"):
        rows.append(("Cuándo se aplica", "Solo durante episodios de contaminación alta"))
    rows.append(("Horario", e(horario(z))))
    if z.get("desde"):
        rows.append(("En vigor desde", fecha(z["desde"])))
    if z.get("descripcion") and len(z["descripcion"]) > 25 and not z["descripcion"].startswith("http"):
        rows.append(("Detalles", e(z["descripcion"])))
    if z.get("info_url", "").startswith("http"):
        rows.append(("Más info", f'<a href="{e(z["info_url"])}" rel="noopener" target="_blank">Web del ayuntamiento</a>'))
    return "<dl>" + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows) + "</dl>"


def resumen(zs):
    if zs and all(z.get("estado") not in (None, "", "active") for z in zs):
        return "ahora mismo no se aplica la zona: pueden entrar todos los coches"
    perm = [z.get("permitidas") for z in zs if z.get("permitidas")]
    if not perm:
        return "consulta qué etiquetas pueden entrar"
    comunes = [k for k in TODAS if all(k in p for p in perm)]
    if comunes == TODAS:
        return "pueden entrar todos los coches"
    if "N" not in comunes and comunes == ["0", "E", "C", "B"]:
        return "no pueden entrar los coches sin etiqueta"
    return "pueden entrar con etiqueta " + ", ".join(NOMBRES[k] for k in comunes) if comunes else "acceso muy restringido"


FOOTER = ('<footer>Datos: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico) y Punto de Acceso Nacional de la DGT (CC BY 4.0) y '
          '© colaboradores de OpenStreetMap (ODbL), actualizados cada día. Web no oficial e informativa: confirma siempre en la web del ayuntamiento.</footer>')


def guias_links(raiz):
    return f'<a href="{raiz}ciudades-abiertas/"><strong>Ciudades más abiertas al visitante</strong></a>' + "".join(f'<a href="{raiz}guias/{g["slug"]}/">{e(g["titulo"])}</a>' for g in GUIAS)


def cabecera(titulo, desc, url, ld):
    return f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{ld}</script>
</head><body><div class="wrap">
"""


def faq_ld(pares):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]},
        ensure_ascii=False).replace("<", "\\u003c")


def pagina_guia(g):
    url = f"{BASE}guias/{g['slug']}/"
    preguntas = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faq"])
    otras = "".join(f'<a href="../{o["slug"]}/">{e(o["titulo"])}</a>' for o in GUIAS if o is not g)
    return (cabecera(g["title"], g["desc"], url, faq_ld(g["faq"]))
            + f"""<p class="muted"><a href="../../">¿Puedo entrar?</a> › <a href="../">Guías</a></p>
<h1>{e(g["titulo"])}</h1>
<p class="muted">Revisado el {fecha(g["revisado"])}.</p>
<section class="card"><h2>¿Puede entrar tu coche?</h2><p>Escribe tu matrícula y te decimos tu etiqueta oficial de la DGT y en qué ciudades puedes entrar.</p>
<form action="../../" method="get"><label class="plate"><span>E</span><input name="q" placeholder="1234BCD" aria-label="Matrícula" maxlength="10" required></label><button type="submit">Comprobar</button></form></section>
{re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\\1" target="_blank" rel="noopener">', g["cuerpo"])}
<section class="card"><h2>Preguntas frecuentes</h2>{preguntas}</section>
<section class="card"><h2>Más guías</h2><p class="guias">{otras}</p></section>
{FOOTER}
</div></body></html>
""")


def indice_guias():
    items = "".join(f'<section class="card"><h2><a href="{g["slug"]}/">{e(g["titulo"])}</a></h2><p class="muted">{e(g["desc"])}</p></section>' for g in GUIAS)
    return (cabecera("Guías sobre zonas de bajas emisiones: multas, etiquetas, ayudas y excepciones",
                     "Guías claras sobre las zonas de bajas emisiones de España: recurrir multas, etiquetas de la DGT, históricos, coches extranjeros, ayudas y preguntas frecuentes.",
                     f"{BASE}guias/", faq_ld([]))
            + f"""<p class="muted"><a href="../">¿Puedo entrar?</a> › Guías</p>
<h1>Guías sobre zonas de bajas emisiones</h1>
{items}
{FOOTER}
</div></body></html>
""")


def abierta(zs):
    """Clasifica una ciudad según lo fácil que es entrar con un coche de fuera.
    Devuelve (grupo, motivo). Grupo 0 = más abierta. Solo usa datos publicados."""
    hoy = date.today().isoformat()
    activas = [z for z in zs if z.get("estado") in (None, "", "active") and not (z.get("desde") and z["desde"] > hoy)]
    if not activas:
        if any(z.get("aviso") for z in zs):
            return 0, "La zona no se aplica ahora mismo (anulada o suspendida)."
        return 0, "La zona aún no se aplica."
    if all(z.get("solo_episodios") for z in activas):
        return 0, "Solo restringe el tráfico en episodios de contaminación alta."
    perm = [z.get("permitidas") for z in activas]
    if any(p is None for p in perm):
        return 9, "Los datos publicados no son claros."
    comunes = [k for k in TODAS if all(k in p for p in perm)]
    def limitado(z):
        h = z.get("horario") or []
        return bool(h) and not any(x.get("de") == "00:00" and x.get("a") in ("23:59", "24:00") for x in h)
    horas = all(limitado(z) for z in activas)
    if "N" in comunes:
        return 0, "Pueden entrar todos los coches."
    if "B" in comunes:
        return 1, "Solo cierra a los coches sin etiqueta" + (", y solo en algunas horas." if horas else ".")
    if "C" in comunes:
        return 2, "Cierra a los coches sin etiqueta y con etiqueta B" + (", pero solo en algunas horas." if horas else ".")
    return 3, "Solo pueden entrar los coches ECO y Cero" + (", y solo en algunas horas." if horas else ".")


GRUPOS = [
    ("Abiertas: puedes entrar con cualquier coche", "Ahora mismo no multan a nadie por su etiqueta, o solo restringen en episodios de contaminación."),
    ("Muy accesibles: solo cierran a los coches sin etiqueta", "Si tu coche tiene cualquier etiqueta (B, C, ECO o Cero), entras."),
    ("Accesibles con etiqueta C o mejor", "Los coches con etiqueta B o sin etiqueta no pueden entrar en la zona."),
    ("Más exigentes", "Solo entran los coches ECO y Cero emisiones."),
]


def pagina_ranking(by):
    grupos = {}
    for c, zs in by.items():
        g, motivo = abierta(zs)
        visit = next((z["excepciones"].get("visitantes") for z in zs if z.get("excepciones") and z["excepciones"].get("visitantes")), None)
        grupos.setdefault(g, []).append((c, motivo, visit))
    bloques = []
    for i, (tit, expl) in enumerate(GRUPOS):
        filas = sorted(grupos.get(i, []), key=lambda x: (x[2] is None, slug(x[0])))
        if not filas:
            continue
        li = "".join(f'<li><a href="../zbe/{slug(c)}/">{e(c)}</a>: {e(m)}' + (f' <strong>Para visitantes:</strong> {e(v)}' if v else "") + "</li>" for c, m, v in filas)
        bloques.append(f'<section class="card"><h2>{e(tit)} ({len(filas)})</h2><p class="muted">{e(expl)}</p><ul>{li}</ul></section>')
    dudosas = sorted(grupos.get(9, []), key=lambda x: slug(x[0]))
    if dudosas:
        bloques.append('<section class="card"><h2>Pendientes de comprobar</h2><p class="muted">Los datos publicados de estas ciudades no son claros. No las clasificamos hasta comprobar su ordenanza.</p><p class="guias">'
                       + "".join(f'<a href="../zbe/{slug(c)}/">{e(c)}</a>' for c, _, _ in dudosas) + "</p></section>")
    n = sum(len(grupos.get(i, [])) for i in range(len(GRUPOS)))
    titulo = "Ciudades más abiertas al visitante: dónde puedes entrar sin miedo a multas"
    desc = "Clasificación de las ciudades españolas con zona de bajas emisiones según lo fácil que es entrar con un coche de fuera. Hecha con datos oficiales y actualizada cada día."
    return (cabecera(titulo, desc, f"{BASE}ciudades-abiertas/", faq_ld([]))
            + f"""<p class="muted"><a href="../">¿Puedo entrar?</a> › Ciudades más abiertas</p>
<h1>Ciudades más abiertas al visitante</h1>
<p>Muchas personas viajan a otras ciudades por trabajo, turismo o para ver a la familia. Aquí ordenamos {n} ciudades con zona de bajas emisiones según lo fácil que se lo ponen a un coche de fuera, de más abierta a más exigente.</p>
<p class="muted">Cómo lo hacemos: solo con los datos publicados por la DGT, OpenStreetMap y los ayuntamientos, sin opiniones. Se actualiza cada día. Si una ciudad tiene permisos especiales para visitantes, lo indicamos. Escribe tu matrícula en <a href="../">el buscador</a> para ver tu caso exacto.</p>
{"".join(bloques)}
{FOOTER}
</div></body></html>
""")


def aplicar_avisos(web, zonas):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avisos.json")
    if not os.path.exists(path):
        return
    avisos = json.load(open(path, encoding="utf-8"))
    for z in zonas:
        a = avisos.get(z["ciudad"])
        if isinstance(a, dict):
            z["aviso"] = a.get("aviso", "")
            z["aviso_fuente"] = a.get("fuente", "")
            if a.get("estado"):
                z["estado"] = a["estado"]
    with open(os.path.join(web, "data", "zonas.json"), "w", encoding="utf-8") as f:
        json.dump(zonas, f, ensure_ascii=False, separators=(",", ":"))


def pagina(ciudad, zs, todas):
    s = slug(ciudad)
    exc = next((z["excepciones"] for z in zs if z.get("excepciones")), None)
    res = resumen(zs)
    titulo = f"ZBE de {ciudad}: ¿puede entrar tu coche? Etiquetas, horario y multas"
    desc = f"Zona de bajas emisiones de {ciudad}: {res}. Escribe tu matrícula y comprueba gratis tu etiqueta de la DGT, el horario y el mapa."
    zonas = "".join(f'<section class="card"><h2>{e(z["zona"]) if z.get("zona") else "Normas de la zona"}</h2>{zona_html(z, ciudad)}</section>' for z in zs)
    if exc:
        excb = (f'<section class="card"><h2>Excepciones</h2><dl><dt>Vehículos históricos</dt><dd>{e(exc.get("historicos"))}</dd>'
                f'<dt>Movilidad reducida</dt><dd>{e(exc.get("pmr"))}</dd>'
                + (f'<dt>Norma</dt><dd><a href="{e(exc["fuente"])}" target="_blank" rel="noopener">Ordenanza municipal</a></dd>' if exc.get("fuente") else "")
                + "</dl></section>")
    else:
        excb = ('<section class="card"><h2>Excepciones</h2><p class="muted">Los vehículos históricos, los de personas con movilidad reducida, '
                'los de emergencia y otros suelen tener excepciones o permisos, pero cada ayuntamiento pone sus condiciones. '
                'Consulta la web del ayuntamiento antes de entrar.</p></section>')
    otras = " · ".join(f'<a href="../{slug(c)}/">{e(c)}</a>' for c in todas if c != ciudad)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"¿Qué coches pueden entrar en la ZBE de {ciudad}?",
             "acceptedAnswer": {"@type": "Answer", "text": f"Según los datos de la DGT, {res}."}},
            {"@type": "Question", "name": f"¿Cuál es el horario de la ZBE de {ciudad}?",
             "acceptedAnswer": {"@type": "Answer", "text": horario(zs[0])}},
            {"@type": "Question", "name": f"¿Cuánto es la multa por entrar en la ZBE de {ciudad}?",
             "acceptedAnswer": {"@type": "Answer", "text": "Normalmente 200 € (100 € con pronto pago), aunque la cuantía la fija cada ayuntamiento."}},
        ]}, ensure_ascii=False).replace("<", "\\u003c")
    return f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}zbe/{s}/">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:url" content="{BASE}zbe/{s}/"><meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Space+Grotesk:wght@700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{ld}</script>
</head><body><div class="wrap">
<p class="muted"><a href="../../">¿Puedo entrar?</a> › Zonas de bajas emisiones › {e(ciudad)}</p>
<h1>Zona de bajas emisiones de {e(ciudad)}</h1>
<p>En la ZBE de {e(ciudad)} {e(res)}. Escribe tu matrícula y te decimos al momento tu etiqueta oficial de la DGT y si puedes entrar.</p>
<section class="card"><h2>¿Puede entrar mi coche?</h2>
<form action="../../" method="get"><label class="plate"><span>E</span><input name="q" placeholder="1234BCD" aria-label="Matrícula" maxlength="10" required></label>
<input type="hidden" name="ciudad" value="{e(ciudad)}"><button type="submit">Comprobar</button></form>
<p class="muted">Gratis y sin registro. No guardamos las matrículas.</p></section>
{zonas}
{excb}
<section class="card"><h2>Multas</h2><p>Entrar en la zona sin cumplir los requisitos suele costar <strong>200 €</strong> (100 € con pronto pago). La cuantía exacta la fija el ayuntamiento de {e(ciudad)}. <a href="../../guias/recurrir-multa-zbe/">Cómo recurrir una multa</a>.</p></section>
<section class="card"><h2>Guías</h2><p class="guias">{guias_links("../../")}</p></section>
<section class="card"><h2>Otras ciudades</h2><p class="muted">{otras}</p></section>
<footer>Datos: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico) y Punto de Acceso Nacional de la DGT (CC BY 4.0) y © colaboradores de OpenStreetMap (ODbL), actualizados cada día. Web no oficial e informativa: confirma siempre en la web del ayuntamiento.</footer>
</div></body></html>
"""


def main(web):
    zonas = json.load(open(os.path.join(web, "data", "zonas.json"), encoding="utf-8"))
    aplicar_avisos(web, zonas)
    by = {}
    for z in zonas:
        by.setdefault(z["ciudad"], []).append(z)
    ciudades = sorted(by, key=slug)
    urls = [BASE]
    for c in ciudades:
        d = os.path.join(web, "zbe", slug(c))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(c, by[c], ciudades))
        urls.append(f"{BASE}zbe/{slug(c)}/")
    os.makedirs(os.path.join(web, "ciudades-abiertas"), exist_ok=True)
    with open(os.path.join(web, "ciudades-abiertas", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_ranking(by))
    urls.append(f"{BASE}ciudades-abiertas/")
    os.makedirs(os.path.join(web, "guias"), exist_ok=True)
    with open(os.path.join(web, "guias", "index.html"), "w", encoding="utf-8") as f:
        f.write(indice_guias())
    urls.append(f"{BASE}guias/")
    for g in GUIAS:
        d = os.path.join(web, "guias", g["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina_guia(g))
        urls.append(f"{BASE}guias/{g['slug']}/")
    hoy = date.today().isoformat()
    with open(os.path.join(web, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"<url><loc>{u}</loc><lastmod>{hoy}</lastmod></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(web, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /data/\nSitemap: {BASE}sitemap.xml\n")
    idx = os.path.join(web, "index.html")
    s = open(idx, encoding="utf-8").read()
    links = " · ".join(f'<a href="zbe/{slug(c)}/">{e(c)}</a>' for c in ciudades)
    s = re.sub(r"<!--CIUDADES-->.*?<!--/CIUDADES-->", f"<!--CIUDADES-->{links}<!--/CIUDADES-->", s, flags=re.S)
    s = re.sub(r"<!--GUIAS-->.*?<!--/GUIAS-->", "<!--GUIAS-->" + guias_links("") + "<!--/GUIAS-->", s, flags=re.S)
    open(idx, "w", encoding="utf-8").write(s)
    print(f"{len(ciudades)} páginas de ciudad")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web")
