#!/usr/bin/env python3
"""Aparcamientos disuasorios (park & ride) cerca de cada zona de bajas emisiones.

Lee web/data/zonas.json, pide a OpenStreetMap los aparcamientos marcados con
park_ride alrededor de cada ciudad y escribe web/data/parkings.json:
{"Ciudad": [{"n": nombre, "lat": .., "lon": .., "pago": "sí|no|", "plazas": "..", "tipo": "bus|tren|.."}]}

Uso: python scripts/build_parkings.py web/data
Datos © colaboradores de OpenStreetMap, licencia ODbL.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_osm import overpass, CACHE  # noqa: E402

MARGEN = 0.06  # unos 6 km alrededor de las zonas
TIPOS = {"bus": "autobús", "train": "tren", "tram": "tranvía", "metro": "metro", "subway": "metro", "yes": ""}


def caja(zs):
    b = [z["bbox"] for z in zs if z.get("bbox")]
    if not b:
        return None
    return (min(x[0] for x in b) - MARGEN, min(x[1] for x in b) - MARGEN,
            max(x[2] for x in b) + MARGEN, max(x[3] for x in b) + MARGEN)


def pedir_todos():
    """Una sola consulta para toda España (unos pocos miles de aparcamientos)."""
    cache = os.path.join(CACHE, "pr_espana.json")
    q = ('[out:json][timeout:180];area["ISO3166-1"="ES"][admin_level=2]->.es;'
         'nwr["park_ride"]["park_ride"!="no"](area.es);out center tags;')
    r = overpass(q, intentos=2, espera=200)
    if r is not None and r.get("elements"):
        os.makedirs(CACHE, exist_ok=True)
        with open(cache, "w") as f:
            json.dump(r["elements"], f)
        return r["elements"], "OSM"
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f), "copia"
    return None, "sin datos"


def dentro(el, bb):
    lat = el.get("lat") or (el.get("center") or {}).get("lat")
    lon = el.get("lon") or (el.get("center") or {}).get("lon")
    return lat is not None and lon is not None and bb[0] <= lat <= bb[2] and bb[1] <= lon <= bb[3]


def main(out):
    with open(os.path.join(out, "zonas.json"), encoding="utf-8") as f:
        zonas = json.load(f)
    por = {}
    for z in zonas:
        por.setdefault(z["ciudad"], []).append(z)
    res = {}
    todos, origen = pedir_todos()
    print(f"Aparcamientos disuasorios en España: {len(todos or [])} ({origen})")
    if todos is None:
        return
    for ciudad in sorted(por):
        bb = caja(por[ciudad])
        if not bb:
            continue
        lista = []
        for el in (x for x in todos if dentro(x, bb)):
            t = el.get("tags", {})
            lat = el.get("lat") or (el.get("center") or {}).get("lat")
            lon = el.get("lon") or (el.get("center") or {}).get("lon")
            if lat is None or lon is None:
                continue
            fee = t.get("fee", "")
            lista.append({"n": t.get("name") or t.get("official_name") or "",
                          "lat": round(lat, 5), "lon": round(lon, 5),
                          "pago": "sí" if fee not in ("", "no") else ("no" if fee == "no" else ""),
                          "plazas": t.get("capacity", ""),
                          "tipo": ", ".join(TIPOS.get(x.strip(), x.strip()) for x in t.get("park_ride", "").split(";") if TIPOS.get(x.strip(), x.strip()))})
        lista.sort(key=lambda p: (p["n"] == "", p["n"]))
        res[ciudad] = lista[:40]
        print(f"{ciudad}: {len(lista)} aparcamientos")
    with open(os.path.join(out, "parkings.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web/data")
