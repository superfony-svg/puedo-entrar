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
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_osm import overpass, slug, CACHE  # noqa: E402

MARGEN = 0.06  # unos 6 km alrededor de las zonas
LIMITE = time.time() + 480
TIPOS = {"bus": "autobús", "train": "tren", "tram": "tranvía", "metro": "metro", "subway": "metro", "yes": ""}


def caja(zs):
    b = [z["bbox"] for z in zs if z.get("bbox")]
    if not b:
        return None
    return (min(x[0] for x in b) - MARGEN, min(x[1] for x in b) - MARGEN,
            max(x[2] for x in b) + MARGEN, max(x[3] for x in b) + MARGEN)


def pedir(ciudad, bb):
    cache = os.path.join(CACHE, "pr_" + slug(ciudad) + ".json")
    r = None
    if time.time() < LIMITE:
        s, w, n, e = bb
        q = f'[out:json][timeout:60];nwr["park_ride"]["park_ride"!="no"]({s},{w},{n},{e});out center tags;'
        r = overpass(q, intentos=1, espera=60)
    if r is not None:
        os.makedirs(CACHE, exist_ok=True)
        with open(cache, "w") as f:
            json.dump(r.get("elements", []), f)
        return r.get("elements", []), "OSM"
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f), "copia"
    return None, "sin datos"


def main(out):
    with open(os.path.join(out, "zonas.json"), encoding="utf-8") as f:
        zonas = json.load(f)
    por = {}
    for z in zonas:
        por.setdefault(z["ciudad"], []).append(z)
    res = {}
    for ciudad in sorted(por, key=lambda c: os.path.exists(os.path.join(CACHE, "pr_" + slug(c) + ".json"))):
        bb = caja(por[ciudad])
        if not bb:
            continue
        els, origen = pedir(ciudad, bb)
        if els is None:
            print(f"{ciudad}: {origen}")
            continue
        lista = []
        for el in els:
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
        print(f"{ciudad}: {len(lista)} aparcamientos ({origen})")
    with open(os.path.join(out, "parkings.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "web/data")
