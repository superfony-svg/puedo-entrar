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
import urllib.parse
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
.menu{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.92rem;font-weight:600;padding-bottom:10px;border-bottom:1px solid var(--line)}.menu a{text-decoration:none;color:var(--accent)}.menu a:hover{text-decoration:underline}
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
    if z.get("sin_mapa"):
        rows.append(("Mapa", "Aún no tenemos el contorno exacto de la zona: guíate por las señales de entrada."))
    if z.get("permitidas"):
        chips = "".join(
            f'<span class="chip {"ok" if k in z["permitidas"] else "no"}">{"✓" if k in z["permitidas"] else "✗"} {NOMBRES[k]}</span>'
            for k in TODAS)
        rows.append(("Etiquetas", f'<div class="chips">{chips}</div>'))
    else:
        rows.append(("Etiquetas", "Los datos publicados no son claros: consulta la web del ayuntamiento."))
    if z.get("solo_episodios"):
        rows.append(("Cuándo se aplica", "Solo durante episodios de contaminación alta"))
    rows.append(("Horario", e(horario(z))))
    if z.get("desde"):
        rows.append(("En vigor desde", fecha(z["desde"])))
    if z.get("descripcion") and len(z["descripcion"]) > 25 and not z["descripcion"].startswith("http"):
        rows.append(("Detalles", e(z["descripcion"])))
    if z.get("info_url", "").startswith("http"):
        rows.append(("Más info", f'<a href="{e(z["info_url"])}" rel="noopener" target="_blank">Web del ayuntamiento</a>'))
    ok, txt = fiab(z)
    rows.append(("Fuente de este dato", ("✓ " if ok else "⚠ ") + e(txt)
                 + (f' <a href="{e(z["fuente_datos"])}" target="_blank" rel="noopener">Ver resumen</a>' if z.get("fuente_datos", "").startswith("http") else "")))
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


FOOTER = ('<footer>Datos: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico); Punto de Acceso Nacional de la DGT '
          '(<a href="https://creativecommons.org/licenses/by/4.0/deed.es" target="_blank" rel="noopener">CC BY 4.0</a>, con cambios de formato y correcciones nuestras) y '
          '<a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© colaboradores de OpenStreetMap</a> (ODbL). '
          'Actualizados el ' + date.today().strftime("%d/%m/%Y") + '. Web no oficial, sin relación con la DGT ni con los ayuntamientos: confirma siempre en la web del ayuntamiento. '
          '<a href="{raiz}aviso-legal/">Aviso legal y privacidad</a>.</footer>')


def guias_links(raiz):
    return f'<a href="{raiz}ciudades-abiertas/"><strong>Ciudades más abiertas al visitante</strong></a>' + "".join(f'<a href="{raiz}guias/{g["slug"]}/">{e(g["titulo"])}</a>' for g in GUIAS)


def menu(raiz):
    return (f'<nav class="menu" aria-label="Menú"><a href="{raiz}">Inicio</a><a href="{raiz}#h-ciu">Ciudades</a><a href="{raiz}ciudades-abiertas/">Ciudades abiertas</a><a href="{raiz}calendario/">Calendario</a>'
            f'<a href="{raiz}guias/">Guías</a><a href="{raiz}guias/preguntas-frecuentes/">Preguntas</a><a href="{raiz}aviso-legal/">Aviso legal</a></nav>')


def cabecera(titulo, desc, url, ld, raiz="../"):
    return f"""<!doctype html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="article"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="manifest" href="{BASE}manifest.webmanifest"><meta name="theme-color" content="#1f6f5c"><link rel="apple-touch-icon" href="{BASE}icons/apple-touch-icon.png">
<style>{CSS}</style>
<script type="application/ld+json">{ld}</script>
</head><body><div class="wrap">
{menu(raiz)}
"""


def faq_ld(pares):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]},
        ensure_ascii=False).replace("<", "\\u003c")


def pagina_guia(g):
    url = f"{BASE}guias/{g['slug']}/"
    preguntas = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faq"])
    otras = "".join(f'<a href="../{o["slug"]}/">{e(o["titulo"])}</a>' for o in GUIAS if o is not g)
    return (cabecera(g["title"], g["desc"], url, faq_ld(g["faq"]), "../../")
            + f"""<p class="muted"><a href="../../">¿Puedo entrar?</a> › <a href="../">Guías</a></p>
<h1>{e(g["titulo"])}</h1>
<p class="muted">Revisado el {fecha(g["revisado"])}.</p>
<section class="card"><h2>¿Puede entrar tu coche?</h2><p>Escribe tu matrícula y te decimos tu etiqueta oficial de la DGT y en qué ciudades puedes entrar.</p>
<form action="../../" method="get"><label class="plate"><span>E</span><input name="q" placeholder="1234BCD" aria-label="Matrícula" maxlength="10" required></label><button type="submit">Comprobar</button></form></section>
{re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\\1" target="_blank" rel="noopener">', g["cuerpo"])}
<section class="card"><h2>Preguntas frecuentes</h2>{preguntas}</section>
<section class="card"><h2>Más guías</h2><p class="guias">{otras}</p></section>
{FOOTER.format(raiz='../../')}
</div></body></html>
""")


def fiab(z):
    if z.get("aviso"):
        return False, "Aviso puesto por nosotros a partir de noticias: confírmalo en el ayuntamiento."
    if z.get("fuente") == "osm":
        return False, "OpenStreetMap (mapa colaborativo hecho por voluntarios). Sin verificar con la ordenanza municipal."
    if z.get("fuente") == "manual":
        return False, "Resumen de terceros. Sin verificar con la ordenanza municipal."
    if z.get("corregido"):
        return False, "Dato de la DGT corregido a mano por nosotros porque se contradecía."
    return True, "Oficial: publicado por la DGT en su Punto de Acceso Nacional" + (f" (versión del {fecha(z['version'])})." if z.get("version") else ".")


def aviso_legal():
    return (cabecera("Aviso legal y privacidad · ¿Puedo entrar?", "Condiciones de uso, responsabilidad, fuentes de datos y privacidad de ¿Puedo entrar?.", f"{BASE}aviso-legal/", faq_ld([]))
            + f"""<p class="muted"><a href="../">¿Puedo entrar?</a> › Aviso legal</p>
<h1>Aviso legal y privacidad</h1>
<p class="muted">Actualizado el {fecha(date.today().isoformat())}.</p>
<section class="card"><h2>Qué es esta web</h2>
<p>¿Puedo entrar? es una web <strong>informativa y no oficial</strong>. No tiene relación con la Dirección General de Tráfico (DGT) ni con ningún ayuntamiento.</p></section>
<section class="card"><h2>La información es orientativa</h2>
<ul>
<li>Juntamos datos públicos: el fichero de etiquetas de la DGT, las zonas que publica la DGT en su Punto de Acceso Nacional, el mapa colaborativo OpenStreetMap y resúmenes de normas.</li>
<li>Estos datos pueden tener errores, estar incompletos o no estar al día. En cada ciudad indicamos de dónde sale cada dato y si está verificado con la norma oficial.</li>
<li>Lo que vale es la <strong>ordenanza municipal</strong> publicada en el boletín oficial y las <strong>señales</strong> de la zona. Ante cualquier duda, manda lo que diga el ayuntamiento.</li>
<li>Usar esta web no da derecho a entrar en ninguna zona ni sirve como justificante ante una multa.</li>
</ul></section>
<section class="card"><h2>Responsabilidad</h2>
<p>Hacemos lo posible para que la información sea correcta y esté al día, pero no podemos garantizarlo. Comprueba siempre la norma oficial antes de entrar en una zona de bajas emisiones. No respondemos de las sanciones o daños que se deriven de decisiones tomadas solo con la información de esta web, salvo en lo que la ley no permita excluir.</p>
<p>Las guías explican de forma general cómo funcionan las multas, las ayudas y las excepciones. No son asesoramiento jurídico para un caso concreto.</p></section>
<section class="card"><h2>Titular</h2>
<p>¿Puedo entrar? es un proyecto personal, gratuito y sin publicidad. Si en el futuro tiene publicidad o ingresos, aquí aparecerán el nombre, el NIF, el domicilio y el correo de contacto del titular, como exige la Ley de Servicios de la Sociedad de la Información (LSSI). Mientras tanto, puedes contactar por el enlace de «Errores y contacto».</p></section>
<section class="card"><h2>Privacidad</h2>
<ul>
<li><strong>No tenemos servidores propios ni base de datos:</strong> no recogemos ni guardamos datos personales. No hay registro, ni cookies, ni analítica, ni publicidad.</li>
<li><strong>Matrícula:</strong> la búsqueda se hace en tu propio navegador. Tu navegador descarga un fichero con miles de matrículas que empiezan igual que la tuya y busca la tuya dentro. La matrícula completa no sale de tu dispositivo.</li>
<li><strong>Ubicación:</strong> solo se usa si pulsas «¿Dónde estoy?» y das permiso. Se queda en tu dispositivo y no se envía a nadie.</li>
<li><strong>Municipio del impuesto:</strong> si lo eliges, se guarda solo en tu navegador (almacenamiento local) para recordarlo la próxima vez. Es una preferencia que pides tú, por lo que no necesita aviso de cookies. Se borra al borrar los datos del sitio en tu navegador.</li>
<li><strong>Servicios de terceros:</strong> la web está alojada en GitHub Pages (GitHub, Inc.) y el mapa usa las imágenes de OpenStreetMap y la librería Leaflet desde cdnjs (Cloudflare). Como en cualquier web, esos servidores reciben tu dirección IP y los ficheros que pide tu navegador, según sus propias políticas de privacidad.</li>
<li><strong>Planificador de viaje:</strong> si lo usas, el origen y el destino que escribes se envían a Nominatim (OpenStreetMap) para encontrarlos y a OSRM para calcular la ruta, según sus propias políticas. No los guardamos.</li>
<li><strong>Si nos avisas de un error</strong> en GitHub, tu mensaje es público y lo gestiona GitHub. Solo lo usamos para corregir el dato.</li>
</ul></section>
<section class="card"><h2>Fuentes, licencias y reutilización</h2>
<ul>
<li><strong>Etiquetas:</strong> fichero de distintivos ambientales de la Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico), que reutilizamos según sus condiciones y la Ley 37/2007 de reutilización de la información del sector público. Citamos la fuente, indicamos la fecha de actualización, no alteramos los datos (solo traducimos el código, por ejemplo 16MC, a su nombre, C) y la DGT no patrocina ni colabora con esta web. Esta información se puede consultar gratis en la <a href="https://sede.dgt.gob.es/es/vehiculos/informacion-de-vehiculos/distintivo-ambiental/" target="_blank" rel="noopener">sede de la DGT</a> (<a href="https://sede.dgt.gob.es/es/contenido/derechos-sobre-la-propiedad-intelectual/index.html" target="_blank" rel="noopener">condiciones de uso</a>).</li>
<li><strong>Zonas de la DGT:</strong> Punto de Acceso Nacional de la DGT (nap.dgt.es), licencia <a href="https://creativecommons.org/licenses/by/4.0/deed.es" target="_blank" rel="noopener">CC BY 4.0</a>. Hemos cambiado el formato y corregido a mano algunos datos que se contradecían; cada ciudad indica cuándo un dato está corregido.</li>
<li><strong>Zonas de OpenStreetMap y mapa:</strong> <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© colaboradores de OpenStreetMap</a>. Los contornos de zonas sacados de OpenStreetMap se ofrecen bajo la licencia <a href="https://opendatacommons.org/licenses/odbl/" target="_blank" rel="noopener">ODbL</a>.</li>
<li><strong>Textos de esta web:</strong> redactados por nosotros. Los datos de normas que tomamos de resúmenes de terceros se indican en cada ciudad como «sin verificar».</li>
</ul></section>
<section class="card"><h2>Errores y contacto</h2>
<p>Si ves un dato mal, <a href="https://github.com/superfony-svg/puedo-entrar/issues/new?title=Error%20en%20los%20datos" target="_blank" rel="noopener">avísanos aquí</a>, con el enlace a la norma oficial si puedes. Lo revisaremos y corregiremos lo antes posible.</p></section>
{FOOTER.format(raiz='../')}
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
{FOOTER.format(raiz='../')}
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


def pagina_ranking(by, pend=()):
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
    if pend:
        bloques.append(f'<section class="card"><h2>Sin datos todavía ({len(pend)})</h2><p class="muted">Municipios obligados a tener zona de bajas emisiones de los que aún no tenemos las normas. Toca uno para ver lo que sabemos.</p><p class="guias">'
                       + "".join(f'<a href="../zbe/{slug(m["ciudad"])}/">{e(m["ciudad"])}</a>' for m in sorted(pend, key=lambda m: slug(m["ciudad"]))) + "</p></section>")
    n = sum(len(grupos.get(i, [])) for i in range(len(GRUPOS)))
    titulo = "Ciudades más abiertas al visitante: dónde puedes entrar sin miedo a multas"
    desc = "Clasificación de las ciudades españolas con zona de bajas emisiones según lo fácil que es entrar con un coche de fuera. Hecha con datos oficiales y actualizada cada día."
    return (cabecera(titulo, desc, f"{BASE}ciudades-abiertas/", faq_ld([]))
            + f"""<p class="muted"><a href="../">¿Puedo entrar?</a> › Ciudades más abiertas</p>
<h1>Ciudades más abiertas al visitante</h1>
<p>Muchas personas viajan a otras ciudades por trabajo, turismo o para ver a la familia. Aquí ordenamos {n} ciudades con zona de bajas emisiones según lo fácil que se lo ponen a un coche de fuera, de más abierta a más exigente.</p>
<p class="muted">Cómo lo hacemos: solo con los datos publicados por la DGT, OpenStreetMap y los ayuntamientos, sin opiniones. Se actualiza cada día. Si una ciudad tiene permisos especiales para visitantes, lo indicamos. Escribe tu matrícula en <a href="../">el buscador</a> para ver tu caso exacto.</p>
{"".join(bloques)}
{FOOTER.format(raiz='../')}
</div></body></html>
""")


def añadir_manuales(zonas):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "manuales.json")
    if not os.path.exists(path):
        return
    man = json.load(open(path, encoding="utf-8"))
    exc = json.load(open(os.path.join(here, "excepciones.json"), encoding="utf-8"))
    ya = {z["ciudad"] for z in zonas}
    for ciudad, m in man.items():
        if ciudad.startswith("_") or ciudad in ya:
            continue
        z = {"id": slug(ciudad + "-" + m.get("zona", "") + "-manual")[:80], "ciudad": ciudad, "zona": m.get("zona", ""),
             "estado": "active", "permitidas": m.get("permitidas"), "dato_dudoso": not m.get("permitidas"),
             "solo_episodios": m.get("solo_episodios", False), "descripcion": m.get("descripcion", ""),
             "horario": m.get("horario", []), "desde": m.get("desde", ""), "info_url": m.get("info_url", ""),
             "version": m.get("revisado", ""), "bbox": m["bbox"], "fuente": "manual", "sin_mapa": True,
             "fuente_datos": m.get("fuente_datos", "")}
        if ciudad in exc:
            z["excepciones"] = exc[ciudad]
        zonas.append(z)
    zonas.sort(key=lambda z: (slug(z["ciudad"]), z["zona"]))


def aplicar_avisos(web, zonas):
    añadir_manuales(zonas)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avisos.json")
    avisos = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    for z in zonas:
        a = avisos.get(z["ciudad"])
        if isinstance(a, dict):
            z["aviso"] = a.get("aviso", "")
            z["aviso_fuente"] = a.get("fuente", "")
            if a.get("estado"):
                z["estado"] = a["estado"]
    with open(os.path.join(web, "data", "zonas.json"), "w", encoding="utf-8") as f:
        json.dump(zonas, f, ensure_ascii=False, separators=(",", ":"))


def pagina_calendario(by, pend=()):
    """Calendario: desde cuándo se aplica cada zona, cuáles llegan pronto y cuáles están suspendidas."""
    hoy = date.today().isoformat()
    pronto, vigor, sinfecha, avisos, episodios = [], [], [], [], []
    for c, zs in by.items():
        enlace = f'<a href="../zbe/{slug(c)}/">{e(c)}</a>'
        aviso = next((z for z in zs if z.get("aviso")), None)
        if aviso:
            avisos.append((c, f'<li>{enlace}: {e(aviso["aviso"])}</li>'))
            continue
        if all(z.get("solo_episodios") for z in zs):
            episodios.append((c, f"<li>{enlace}</li>"))
            continue
        fechas = sorted(z["desde"] for z in zs if z.get("desde"))
        fut = [f for f in fechas if f > hoy]
        if fut and not [f for f in fechas if f <= hoy]:
            pronto.append((fut[0], f"<li><strong>{fecha(fut[0])}</strong> · {enlace}</li>"))
        elif fechas:
            pas = [f for f in fechas if f <= hoy]
            vigor.append((pas[-1], f"<li>{fecha(pas[0])} · {enlace}</li>"))
        else:
            sinfecha.append((c, f"<li>{enlace}</li>"))
    bloques = []

    def bloque(tit, expl, filas, rev=False):
        if filas:
            li = "".join(x for _, x in sorted(filas, key=lambda r: r[0], reverse=rev))
            bloques.append(f'<section class="card"><h2>{tit} ({len(filas)})</h2><p class="muted">{expl}</p><ul>{li}</ul></section>')
    bloque("Próximamente", "Zonas que empiezan a aplicarse en la fecha indicada, según los datos publicados.", pronto)
    bloque("Suspendidas o con aviso", "Zonas anuladas por un juez, suspendidas o con cambios anunciados. Mira el aviso antes de ir.", sorted(avisos))
    bloque("En vigor", "Fecha desde la que se aplica cada zona según la DGT o el ayuntamiento. Algunas ciudades empiezan con un periodo de aviso sin multa: lo indicamos en su página cuando lo sabemos.", vigor, rev=True)
    bloque("En vigor sin fecha publicada", "Zonas activas en los datos oficiales sin fecha de inicio publicada.", sorted(sinfecha))
    bloque("Solo en episodios de contaminación", "Solo se restringe el paso cuando el ayuntamiento activa un episodio de contaminación.", sorted(episodios))
    for k, tit in (("vigor", "En vigor según la prensa, sin normas detalladas aún"), ("tramite", "En trámite"), ("pendiente", "Sin empezar los trámites"), ("", "Obligadas, sin información")):
        ms = sorted((m for m in pend if m.get("estado_prensa", "") == k), key=lambda m: slug(m["ciudad"]))
        if ms:
            bloques.append(f'<section class="card"><h2>{tit} ({len(ms)})</h2><p class="muted">Según la prensa (Motor16, 31 de marzo de 2026). Sin verificar con la ordenanza.</p><p class="guias">'
                           + "".join(f'<a href="../zbe/{slug(m["ciudad"])}/">{e(m["ciudad"])}</a>' for m in ms) + "</p></section>")
    titulo = "Calendario de las zonas de bajas emisiones: desde cuándo multa cada ciudad"
    desc = "Fechas de inicio de las zonas de bajas emisiones de España, las que llegan pronto, las suspendidas y las que siguen en trámite. Actualizado cada día."
    return (cabecera(titulo, desc, f"{BASE}calendario/", faq_ld([]))
            + f"""<p class="muted"><a href="../">¿Puedo entrar?</a> › Calendario</p>
<h1>Calendario de las zonas de bajas emisiones</h1>
<p>Desde cuándo se aplica cada zona, cuáles llegan pronto y cuáles están suspendidas. Hecho con los datos de la DGT, los ayuntamientos y la prensa, y actualizado cada día.</p>
{"".join(bloques)}
{FOOTER.format(raiz='../')}
</div></body></html>
""")


ESTADO_PRENSA = {
    "vigor": "Según la prensa (Motor16, 31 de marzo de 2026), {c} ya tiene la zona de bajas emisiones en vigor. Aún no tenemos sus normas detalladas (etiquetas, horario y mapa).",
    "tramite": "Según la prensa (Motor16, 31 de marzo de 2026), la zona de bajas emisiones de {c} estaba en trámite: aprobada o en preparación, pero no del todo en marcha.",
    "pendiente": "Según la prensa (Motor16, 31 de marzo de 2026), {c} aún no había empezado los trámites de su zona de bajas emisiones o no lo había comunicado.",
    "": "{c} está obligada por la Ley de Cambio Climático a tener una zona de bajas emisiones. Aún no hemos comprobado si ya está en vigor ni si multa.",
}


def cubierta(m, ciudades):
    a = slug(m)
    return any(a == b or b.startswith(a + "-") or b.endswith("-" + a) for b in map(slug, ciudades))


def pendientes(ciudades):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "municipios.json")
    if not os.path.exists(path):
        return []
    ms = json.load(open(path, encoding="utf-8"))["municipios"]
    return [m for m in ms if not cubierta(m["ciudad"], ciudades)]


def pagina_basica(m, todas):
    c = m["ciudad"]
    s = slug(c)
    estado = ESTADO_PRENSA.get(m.get("estado_prensa", ""), ESTADO_PRENSA[""]).format(c=c)
    titulo = f"ZBE de {c}: ¿está en vigor? Etiquetas y multas"
    desc = f"Zona de bajas emisiones de {c}: estado y qué hacer antes de ir. Comprueba gratis la etiqueta de tu coche con la matrícula."
    otras = " · ".join(f'<a href="../{slug(x)}/">{e(x)}</a>' for x in todas if x != c)
    ld = faq_ld([(f"¿Tiene {c} zona de bajas emisiones?", estado)])
    return (cabecera(titulo, desc, f"{BASE}zbe/{s}/", ld, "../../")
            + f"""<p class="muted"><a href="../../">¿Puedo entrar?</a> › Zonas de bajas emisiones › {e(c)}</p>
<h1>Zona de bajas emisiones de {e(c)}</h1>
<section class="card"><h2>Estado</h2><p>{e(estado)}</p>
<dl><dt>Comunidad</dt><dd>{e(m.get("ccaa", ""))}</dd><dt>Fuente de este dato</dt><dd>⚠ Prensa y listados públicos. Sin verificar con la ordenanza municipal.</dd></dl></section>
<section class="card"><h2>Qué hacer antes de ir</h2><ol>
<li>Comprueba tu etiqueta con la matrícula (abajo).</li>
<li>Busca «zona de bajas emisiones» en la web del Ayuntamiento de {e(c)} y mira qué etiquetas pueden entrar y desde cuándo multan.</li>
<li>Si tu coche tiene etiqueta C, ECO o Cero, en casi todas las zonas de España puedes entrar.</li>
</ol></section>
<section class="card"><h2>¿Puede entrar mi coche?</h2>
<form action="../../" method="get"><label class="plate"><span>E</span><input name="q" placeholder="1234BCD" aria-label="Matrícula" maxlength="10" required></label><button type="submit">Comprobar</button></form>
<p class="muted">Gratis y sin registro. No guardamos las matrículas.</p></section>
<section class="card"><h2>¿Sabes cómo está la zona de {e(c)}?</h2><p class="muted">Si conoces la ordenanza o ves que ya multan, <a href="https://github.com/superfony-svg/puedo-entrar/issues/new?title={urllib.parse.quote("Datos de " + c)}" target="_blank" rel="noopener">avísanos</a> y la completamos.</p></section>
<section class="card"><h2>Guías</h2><p class="guias">{guias_links("../../")}</p></section>
<section class="card"><h2>Otras ciudades</h2><p class="muted">{otras}</p></section>
<p><a href="https://wa.me/?text={urllib.parse.quote("Zona de bajas emisiones de " + c + ": qué coches pueden entrar, horario y multas. " + BASE + "zbe/" + slug(c) + "/")}" target="_blank" rel="noopener">Compartir por WhatsApp</a></p>
{FOOTER.format(raiz='../../')}
</div></body></html>
""")


PARKINGS = {}


def FUENTE_TXT(url):
    for dom, txt in (("race.es", "Resumen del RACE"), ("cecobi.es", "Resumen de la ordenanza (CECOBI)"), ("turismoa.eus", "Oficina de turismo")):
        if dom in url:
            return txt
    return "Ordenanza o web del ayuntamiento"


def si_no_puedes(ciudad, exc):
    """Qué hacer si tu coche no puede entrar: permiso de visitante y aparcamientos fuera de la zona."""
    partes = []
    if exc and exc.get("visitantes"):
        tr = f' <a href="{e(exc["tramite"])}" target="_blank" rel="noopener">Hacer el trámite</a>' if exc.get("tramite") else ""
        partes.append(f'<h3>Permiso para visitantes</h3><p>{e(exc["visitantes"])}{tr}</p>')
    ps = PARKINGS.get(ciudad) or []
    if ps:
        li = []
        for p in ps:
            nombre = p["n"] or "Aparcamiento disuasorio"
            det = [x for x in (("en " + p["tipo"]) if p["tipo"] else "",
                               f'{p["plazas"]} plazas' if p["plazas"] else "",
                               "gratis" if p["pago"] == "no" else ("de pago" if p["pago"] == "sí" else "")) if x]
            url = f'https://www.openstreetmap.org/?mlat={p["lat"]}&mlon={p["lon"]}#map=17/{p["lat"]}/{p["lon"]}'
            ir = f'https://www.google.com/maps/dir/?api=1&destination={p["lat"]},{p["lon"]}'
            li.append(f'<li><a href="{url}" target="_blank" rel="noopener">{e(nombre)}</a>'
                      + (f' <span class="muted">({e(", ".join(det))})</span>' if det else "")
                      + f' · <a href="{ir}" target="_blank" rel="noopener">Cómo llegar</a></li>')
        partes.append('<h3>Aparcamientos disuasorios</h3><p class="muted">Aparcamientos para dejar el coche y seguir en transporte público, '
                      'según OpenStreetMap. Comprueba en el mapa que quedan fuera de la zona y si hay que pagar.</p><ul>' + "".join(li) + "</ul>")
    else:
        partes.append('<h3>Aparcamientos</h3><p class="muted">Aún no tenemos aparcamientos disuasorios marcados en esta ciudad. '
                      'Busca un aparcamiento fuera del límite de la zona (mira el mapa) y sigue en transporte público.</p>')
    partes.append('<p class="muted">Los aparcamientos públicos dentro de la zona a veces dejan entrar a cualquier coche para aparcar: '
                  'compruébalo en la ordenanza antes, porque no pasa en todas las ciudades.</p>')
    return f'<section class="card"><h2>Si tu coche no puede entrar</h2>{"".join(partes)}</section>'


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
                + (f'<dt>Coches de vecinos</dt><dd>{e(exc["residentes"])}</dd>' if exc.get("residentes") else "")
                + (f'<dt>Fuente</dt><dd><a href="{e(exc["fuente"])}" target="_blank" rel="noopener">{FUENTE_TXT(exc["fuente"])}</a> <span class="muted">(revisado el {fecha(exc.get("revisado", ""))})</span></dd>' if exc.get("fuente") else "")
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
<link rel="manifest" href="{BASE}manifest.webmanifest"><meta name="theme-color" content="#1f6f5c"><link rel="apple-touch-icon" href="{BASE}icons/apple-touch-icon.png">
<style>{CSS}</style>
<script type="application/ld+json">{ld}</script>
</head><body><div class="wrap">
{menu("../../")}
<p class="muted"><a href="../../">¿Puedo entrar?</a> › Zonas de bajas emisiones › {e(ciudad)}</p>
<h1>Zona de bajas emisiones de {e(ciudad)}</h1>
<p>En la ZBE de {e(ciudad)} {e(res)}. Escribe tu matrícula y te decimos al momento tu etiqueta oficial de la DGT y si puedes entrar.</p>
<section class="card"><h2>¿Puede entrar mi coche?</h2>
<form action="../../" method="get"><label class="plate"><span>E</span><input name="q" placeholder="1234BCD" aria-label="Matrícula" maxlength="10" required></label>
<input type="hidden" name="ciudad" value="{e(ciudad)}"><button type="submit">Comprobar</button></form>
<p class="muted">Gratis y sin registro. No guardamos las matrículas.</p></section>
{zonas}
{excb}
{si_no_puedes(ciudad, exc)}
<section class="card"><h2>Multas</h2><p>Entrar en la zona sin cumplir los requisitos suele costar <strong>200 €</strong> (100 € con pronto pago). La cuantía exacta la fija el ayuntamiento de {e(ciudad)}. <a href="../../guias/recurrir-multa-zbe/">Cómo recurrir una multa</a>.</p></section>
<section class="card"><h2>Guías</h2><p class="guias">{guias_links("../../")}</p></section>
<section class="card"><h2>¿Has visto un error?</h2><p class="muted">Las normas cambian. Si algo no cuadra con la ordenanza o las señales, <a href="https://github.com/superfony-svg/puedo-entrar/issues/new?title={urllib.parse.quote("Error en " + ciudad)}" target="_blank" rel="noopener">avísanos</a> y lo corregimos.</p></section>
<section class="card"><h2>Otras ciudades</h2><p class="muted">{otras}</p></section>
<p><a href="https://wa.me/?text={urllib.parse.quote("Zona de bajas emisiones de " + ciudad + ": qué coches pueden entrar, horario y multas. " + BASE + "zbe/" + slug(ciudad) + "/")}" target="_blank" rel="noopener">Compartir por WhatsApp</a></p>
{FOOTER.format(raiz='../../')}
</div></body></html>
"""


def main(web):
    zonas = json.load(open(os.path.join(web, "data", "zonas.json"), encoding="utf-8"))
    aplicar_avisos(web, zonas)
    try:
        PARKINGS.update(json.load(open(os.path.join(web, "data", "parkings.json"), encoding="utf-8")))
    except (OSError, ValueError):
        pass
    by = {}
    for z in zonas:
        by.setdefault(z["ciudad"], []).append(z)
    pend = pendientes(list(by))
    with open(os.path.join(web, "data", "pendientes.json"), "w", encoding="utf-8") as f:
        json.dump(pend, f, ensure_ascii=False, separators=(",", ":"))
    ciudades = sorted(by, key=slug)
    todas = sorted(list(by) + [m["ciudad"] for m in pend], key=slug)
    urls = [BASE]
    for c in ciudades:
        d = os.path.join(web, "zbe", slug(c))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(c, by[c], todas))
        urls.append(f"{BASE}zbe/{slug(c)}/")
    for m in pend:
        d = os.path.join(web, "zbe", slug(m["ciudad"]))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina_basica(m, todas))
        urls.append(f"{BASE}zbe/{slug(m['ciudad'])}/")
    os.makedirs(os.path.join(web, "aviso-legal"), exist_ok=True)
    with open(os.path.join(web, "aviso-legal", "index.html"), "w", encoding="utf-8") as f:
        f.write(aviso_legal())
    os.makedirs(os.path.join(web, "ciudades-abiertas"), exist_ok=True)
    with open(os.path.join(web, "ciudades-abiertas", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_ranking(by, pend))
    urls.append(f"{BASE}ciudades-abiertas/")
    os.makedirs(os.path.join(web, "calendario"), exist_ok=True)
    with open(os.path.join(web, "calendario", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_calendario(by, pend))
    urls.append(f"{BASE}calendario/")
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
    links = (f"{len(todas)} municipios: " + " · ".join(f'<a href="zbe/{slug(c)}/">{e(c)}</a>' for c in todas))
    s = re.sub(r"<!--CIUDADES-->.*?<!--/CIUDADES-->", f"<!--CIUDADES-->{links}<!--/CIUDADES-->", s, flags=re.S)
    s = re.sub(r"<!--GUIAS-->.*?<!--/GUIAS-->", "<!--GUIAS-->" + guias_links("") + "<!--/GUIAS-->", s, flags=re.S)
    open(idx, "w", encoding="utf-8").write(s)
    print(f"{len(ciudades)} páginas de ciudad con datos y {len(pend)} básicas")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web")
