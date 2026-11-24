#!/usr/bin/env python3
"""Convierte los ficheros DATEX II de zonas de bajas emisiones de la DGT
(nap.dgt.es, licencia CC BY 4.0) en datos sencillos para la web.

Uso:
    python scripts/build_zonas.py <carpeta_con_xml> <carpeta_salida>

Salida:
  zonas.json          índice: una entrada por zona, sin polígonos
  zonas/<id>.json     polígonos de cada zona: [[[lat, lon], ...], ...]
Etiquetas: 0, E (ECO), C, B, N (sin etiqueta).
"""
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

CIUDADES = {
    "ACoruña": "A Coruña", "AlcalaDeHenares": "Alcalá de Henares", "Alicante": "Alicante",
    "Avila": "Ávila", "Barcelona": "Barcelona", "Benidorm": "Benidorm", "Bilbao": "Bilbao",
    "Cartagena": "Cartagena", "Castellon": "Castellón de la Plana",
    "CerdanyolaDelValles": "Cerdanyola del Vallès", "Donostia-SanSebastian": "Donostia / San Sebastián",
    "DosHermanas": "Dos Hermanas", "ElPratDeLlobregat": "El Prat de Llobregat",
    "Fuenlabrada": "Fuenlabrada", "Gava": "Gavà", "Girona": "Girona", "Granada": "Granada",
    "Granollers": "Granollers", "LasRozas": "Las Rozas de Madrid", "Lleida": "Lleida",
    "Madrid": "Madrid", "Malaga": "Málaga", "Manlleu": "Manlleu", "Mataro": "Mataró",
    "MolinaDeSegura": "Molina de Segura", "Motril": "Motril", "Oviedo": "Oviedo", "Palma": "Palma",
    "PamplonaEnsanche": "Pamplona", "Pontevedra": "Pontevedra", "Reus": "Reus",
    "RondasDeBarcelona": "Barcelona (Rondas)", "Rubi": "Rubí", "Sabadell": "Sabadell",
    "Salamanca": "Salamanca", "SantBoiDeLlobregat": "Sant Boi de Llobregat",
    "SantCugatDelValles": "Sant Cugat del Vallès", "SantJoanDespi": "Sant Joan Despí",
    "SevillaCartuja": "Sevilla (Cartuja)", "Tarragona": "Tarragona", "Terrasa": "Terrassa",
    "Torremolinos": "Torremolinos", "Valencia": "València", "Valladolid": "Valladolid",
    "Viladecans": "Viladecans", "VitoriaGasteiz": "Vitoria-Gasteiz",
}
TODAS = ["0", "E", "C", "B", "N"]
PERIODOS = {"L": "Días laborables", "F": "Festivos", "S": "Sábados", "D": "Domingos"}
EPISODIO = re.compile(r"sin restricciones mientras|(solo|únicamente|unicamente)[^.]{0,40}episodio", re.I)
LIBRE = re.compile(r"^\s*acceso libre", re.I)
ORDEN = ["0", "E", "C", "B", "N"]


def local(tag):
    return tag.rsplit("}", 1)[-1]


def kids(el, name):
    return [c for c in el if local(c.tag) == name]


def find_all(el, name):
    return [c for c in el.iter() if local(c.tag) == name]


def text_of(el, name):
    for c in el.iter():
        if local(c.tag) == name and c.text and c.text.strip():
            return c.text.strip()
    return ""


def value_of(el):
    for c in el.iter():
        if local(c.tag) == "value" and c.text:
            return c.text.strip()
    return ""


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def sticker(v):
    u = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode().upper().strip()
    if u in ("0", "CERO", "CERO EMISIONES", "0 EMISIONES"):
        return "0"
    if u == "ECO":
        return "E"
    if u in ("C", "B"):
        return u
    if "SIN" in u or u == "A":
        return "N"
    return None


def restriction(reg):
    """Devuelve (permitidas, dudoso) a partir de las condiciones de etiqueta."""
    for cs in find_all(reg, "conditions"):
        stick = [c for c in kids(cs, "conditions") if text_of(c, "type") == "stickerCondition"]
        if not stick:
            continue
        negate = any((n.text or "").strip() == "true" for n in kids(cs, "negate"))
        vals = {sticker(value_of(kids(c, "condition")[0])) for c in stick if kids(c, "condition")}
        vals.discard(None)
        if not vals:
            continue
        if "N" in vals:  # la lista nombra las prohibidas (así lo usan varios ayuntamientos)
            return [x for x in TODAS if x not in vals], negate
        if negate:  # "no pueden entrar salvo..." -> la lista son las permitidas
            return [x for x in TODAS if x in vals], False
        return [x for x in TODAS if x not in vals], False
    return None, True


def coherent(perm):
    """Si una etiqueta puede entrar, las más limpias también. Si no se cumple,
    o no queda ninguna permitida, el dato de la DGT no es fiable."""
    if not perm:
        return None
    idx = [ORDEN.index(x) for x in perm]
    if sorted(idx) != list(range(max(idx) + 1)):
        return None
    return perm


def schedule(reg):
    out = []
    for vp in find_all(reg, "validPeriod"):
        name = ""
        for pn in kids(vp, "periodName"):
            name = value_of(pn)
        start, end = text_of(vp, "startTimeOfPeriod"), text_of(vp, "endTimeOfPeriod")
        out.append({
            "dias": PERIODOS.get(name, name or "Todos los días"),
            "de": start[:5] if start else "",
            "a": end[:5] if end else "",
        })
    return out


def polygons(reg):
    polys = []
    for corners in find_all(reg, "openlrPolygonCorners"):
        pts = []
        for c in kids(corners, "openlrCoordinates"):
            try:
                pts.append([round(float(text_of(c, "latitude")), 5), round(float(text_of(c, "longitude")), 5)])
            except ValueError:
                pass
        if len(pts) > 2 and pts[0] == pts[-1]:
            pts.pop()
        if len(pts) >= 3:
            polys.append(pts)
    return polys


def build(src, out):
    os.makedirs(os.path.join(out, "zonas"), exist_ok=True)
    index = []
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".xml"):
            continue
        base = fn[:-4]
        try:
            from urllib.parse import unquote
            base = unquote(base)
            root = ET.parse(os.path.join(src, fn)).getroot()
        except Exception as e:  # un fichero roto no debe tumbar el resto
            print(f"AVISO: no se pudo leer {fn}: {e}")
            continue
        ciudad = CIUDADES.get(base, base)
        zonas = find_all(root, "controlledZone")
        for z in zonas:
            name = ""
            for n in kids(z, "name"):
                name = value_of(n)
            desc = ""
            for d in kids(z, "controlledZoneDescription"):
                desc = value_of(d)
            status = text_of(z, "status")
            regs = find_all(z, "trafficRegulation")
            polys, permitidas, dudoso, horario = [], None, True, []
            for r in regs:
                polys += polygons(r)
                p, d = restriction(r)
                if p is not None and permitidas is None:
                    permitidas, dudoso = p, d
                horario += schedule(r)
            permitidas = coherent(permitidas)
            if permitidas is None and LIBRE.search(desc or ""):
                permitidas, dudoso = list(TODAS), False
            horario = [h for h in horario if not (h["de"] and h["de"] == h["a"])]
            if desc.strip().lower() == "null":
                desc = ""
            if not polys:
                print(f"AVISO: {ciudad} / {name} sin polígono")
                continue
            zid = slug(ciudad + "-" + (name or z.get("id", "")))[:80]
            lats = [p[0] for poly in polys for p in poly]
            lons = [p[1] for poly in polys for p in poly]
            with open(os.path.join(out, "zonas", zid + ".json"), "w") as f:
                json.dump(polys, f, separators=(",", ":"))
            index.append({
                "id": zid,
                "ciudad": ciudad,
                "zona": name if len(zonas) > 1 else "",
                "estado": status,
                "permitidas": permitidas,
                "dato_dudoso": dudoso,
                "solo_episodios": bool(EPISODIO.search(desc)),
                "descripcion": desc,
                "horario": horario,
                "desde": text_of(z, "overallStartTime")[:10],
                "info_url": "" if text_of(z, "urlForFurtherInformation").lower() == "null" else text_of(z, "urlForFurtherInformation"),
                "version": text_of(z, "controlledZoneRecordVersionTime")[:10],
                "bbox": [min(lats), min(lons), max(lats), max(lons)],
            })
    corr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "correcciones.json")
    if os.path.exists(corr_path):
        corr = json.load(open(corr_path, encoding="utf-8"))
        for z in index:
            for k, v in corr.get(z["id"], {}).items():
                if k != "motivo":
                    z[k] = v
                    z["corregido"] = True
    index.sort(key=lambda z: (slug(z["ciudad"]), z["zona"]))
    if len(index) < 10 and not os.environ.get("ALLOW_SMALL"):
        raise SystemExit(f"Solo {len(index)} zonas leídas: algo ha fallado")
    with open(os.path.join(out, "zonas.json"), "w") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    return index


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    idx = build(sys.argv[1], sys.argv[2])
    print(f"{len(idx)} zonas en {len({z['ciudad'] for z in idx})} ciudades")
    for z in idx:
        print(f"- {z['ciudad']} {z['zona']!r}: permitidas={z['permitidas']} dudoso={z['dato_dudoso']} episodios={z['solo_episodios']} horario={z['horario']}")
