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
    if z.get("estado") and z["estado"] != "active":
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
    perm = [z.get("permitidas") for z in zs if z.get("permitidas")]
    if not perm:
        return "consulta qué etiquetas pueden entrar"
    comunes = [k for k in TODAS if all(k in p for p in perm)]
    if comunes == TODAS:
        return "pueden entrar todos los coches"
    if "N" not in comunes and comunes == ["0", "E", "C", "B"]:
        return "no pueden entrar los coches sin etiqueta"
    return "pueden entrar con etiqueta " + ", ".join(NOMBRES[k] for k in comunes) if comunes else "acceso muy restringido"


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
<section class="card"><h2>Multas</h2><p>Entrar en la zona sin cumplir los requisitos suele costar <strong>200 €</strong> (100 € con pronto pago). La cuantía exacta la fija el ayuntamiento de {e(ciudad)}.</p></section>
<section class="card"><h2>Otras ciudades</h2><p class="muted">{otras}</p></section>
<footer>Datos: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico) y Punto de Acceso Nacional de la DGT (CC BY 4.0) y © colaboradores de OpenStreetMap (ODbL), actualizados cada día. Web no oficial e informativa: confirma siempre en la web del ayuntamiento.</footer>
</div></body></html>
"""


def main(web):
    zonas = json.load(open(os.path.join(web, "data", "zonas.json"), encoding="utf-8"))
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
    open(idx, "w", encoding="utf-8").write(s)
    print(f"{len(ciudades)} páginas de ciudad")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web")
