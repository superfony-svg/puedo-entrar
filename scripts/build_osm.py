#!/usr/bin/env python3
"""Añade a web/data/zonas.json las zonas de bajas emisiones de OpenStreetMap
listadas en scripts/osm_zonas.json (ciudades que la DGT no publica).

Uso: python scripts/build_osm.py web/data
Datos © colaboradores de OpenStreetMap, licencia ODbL.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
OVERPASS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter"]
DIAS = {"Mo": "lunes", "Tu": "martes", "We": "miércoles", "Th": "jueves", "Fr": "viernes", "Sa": "sábado", "Su": "domingo"}
TODAS = ["0", "E", "C", "B", "N"]


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


CACHE = os.environ.get("OSM_CACHE", "osm_cache")
LIMITE = time.time() + 600  # pasados 10 minutos, solo se usan las copias guardadas


def overpass(query, intentos=2, espera=90):
    """Devuelve la respuesta de Overpass o None si no responde (no rompe la ejecución)."""
    data = urllib.parse.urlencode({"data": query}).encode()
    last = None
    for attempt in range(intentos):
        for url in OVERPASS:
            try:
                req = urllib.request.Request(url, data=data, headers={"User-Agent": "puedo-entrar/1.0"})
                with urllib.request.urlopen(req, timeout=espera) as r:
                    return json.load(r)
            except Exception as e:  # servidores saturados a menudo: reintentar
                last = e
        if attempt + 1 < intentos:
            time.sleep(10)
    print(f"AVISO Overpass no responde: {last}")
    return None


def elemento(key):
    """Pide un elemento a Overpass; si falla, usa la copia guardada de otra noche."""
    t, i = key.split("/")
    cache = os.path.join(CACHE, key.replace("/", "_") + ".json")
    r = None
    if time.time() < LIMITE:
        r = overpass(f"[out:json][timeout:60];{t}(id:{i});out tags geom;", intentos=1, espera=75)
    els = (r or {}).get("elements") or []
    if els:
        os.makedirs(CACHE, exist_ok=True)
        with open(cache, "w") as f:
            json.dump(els[0], f)
        return els[0], "Overpass"
    if r and r.get("remark"):
        print(f"AVISO Overpass {key}: {r['remark']}")
    if os.path.exists(cache):
        return json.load(open(cache)), "copia guardada"
    return None, "sin datos"


def rings_from_ways(ways):
    """Une trozos de borde (listas de puntos) en anillos cerrados."""
    segs = [w[:] for w in ways if len(w) >= 2]
    rings = []
    while segs:
        ring = segs.pop(0)
        changed = True
        while ring[0] != ring[-1] and changed:
            changed = False
            for i, s in enumerate(segs):
                if s[0] == ring[-1]:
                    ring += s[1:]
                elif s[-1] == ring[-1]:
                    ring += list(reversed(s))[1:]
                elif s[-1] == ring[0]:
                    ring = s[:-1] + ring
                elif s[0] == ring[0]:
                    ring = list(reversed(s))[:-1] + ring
                else:
                    continue
                segs.pop(i)
                changed = True
                break
        if len(ring) >= 4:
            if ring[0] == ring[-1]:
                ring = ring[:-1]
            rings.append(ring)
    return rings


def pts(geom):
    return [[round(p["lat"], 5), round(p["lon"], 5)] for p in geom]


def horario(tags):
    raw = tags.get("opening_hours") or ""
    m = re.search(r"no @ \(?([^)]*)\)?", tags.get("access:conditional", ""))
    if not raw and m:
        raw = m.group(1)
    out = []
    for part in raw.split(";"):
        part = part.strip()
        mm = re.match(r"([A-Za-z]{2})(?:-([A-Za-z]{2}))?\s+(\d\d:\d\d)-(\d\d:\d\d)", part)
        if mm and mm.group(1) in DIAS:
            d = DIAS[mm.group(1)] + (" a " + DIAS.get(mm.group(2), mm.group(2)) if mm.group(2) else "")
            out.append({"dias": d[0].upper() + d[1:], "de": mm.group(3), "a": mm.group(4)})
        elif part == "24/7":
            out.append({"dias": "Todos los días", "de": "00:00", "a": "23:59"})
    return out


def permitidas_de(tags):
    note = tags.get("access:note", "")
    if re.fullmatch(r"[A-Z0-9, ]+", note or "-"):
        vals = {"0" if v == "0" else "E" if v == "ECO" else v for v in (x.strip() for x in note.split(","))}
        perm = [k for k in TODAS if k in vals]
        return perm or None
    return None


def main(out):
    conf = json.load(open(os.path.join(HERE, "osm_zonas.json"), encoding="utf-8"))
    conf.pop("_nota", None)
    els = []
    for k in conf:  # uno a uno: si uno falla, los demás siguen
        el, origen = elemento(k)
        print(f"{k} ({conf[k]['ciudad']}): {origen}")
        if el:
            els.append(el)
    idx_path = os.path.join(out, "zonas.json")
    index = json.load(open(idx_path, encoding="utf-8"))
    ya = {z["ciudad"] for z in index if z.get("fuente") != "osm"}
    added = 0
    for el in els:
        key = f'{el["type"]}/{el["id"]}'
        c = conf.get(key)
        if not c or c["ciudad"] in ya:
            continue
        tags = el.get("tags", {})
        if el["type"] == "way":
            polys = [pts(el.get("geometry", []))]
            if polys[0] and polys[0][0] == polys[0][-1]:
                polys[0] = polys[0][:-1]
        else:
            outer = [pts(m["geometry"]) for m in el.get("members", []) if m.get("type") == "way" and m.get("role") in ("outer", "") and m.get("geometry")]
            polys = rings_from_ways(outer)
        polys = [p for p in polys if len(p) >= 3]
        if not polys:
            n = len(el.get("members", [])) if el["type"] == "relation" else len(el.get("geometry", []))
            print(f"AVISO: {key} ({c['ciudad']}) sin geometría válida; miembros/puntos: {n}")
            continue
        lats = [p[0] for poly in polys for p in poly]
        lons = [p[1] for poly in polys for p in poly]
        zid = slug(c["ciudad"] + "-" + c.get("zona", "") + "-osm")[:80]
        with open(os.path.join(out, "zonas", zid + ".json"), "w") as f:
            json.dump(polys, f, separators=(",", ":"))
        desde = tags.get("start_date") or tags.get("opening_date") or ""
        if re.fullmatch(r"\d{4}", desde):
            desde += "-01-01"
        index.append({
            "id": zid,
            "ciudad": c["ciudad"],
            "zona": c.get("zona", ""),
            "estado": "active",
            "permitidas": c.get("permitidas") or permitidas_de(tags),
            "dato_dudoso": "permitidas" not in c,
            "solo_episodios": False,
            "descripcion": tags.get("description", ""),
            "horario": c.get("horario") or horario(tags),
            "desde": desde[:10],
            "info_url": tags.get("website") or tags.get("url") or tags.get("source") or "",
            "version": "",
            "bbox": [min(lats), min(lons), max(lats), max(lons)],
            "fuente": "osm",
        })
        added += 1
        print(f"  + {c['ciudad']} {c.get('zona', '')} ({key}, {len(polys)} anillo/s)")
    exc = json.load(open(os.path.join(HERE, "excepciones.json"), encoding="utf-8"))
    for z in index:
        if z.get("fuente") == "osm" and z["ciudad"] in exc:
            z["excepciones"] = exc[z["ciudad"]]
    index.sort(key=lambda z: (slug(z["ciudad"]), z["zona"]))
    with open(idx_path, "w") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{added} zonas añadidas desde OpenStreetMap")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web/data")
