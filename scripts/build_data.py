#!/usr/bin/env python3
"""Convierte el fichero de distintivos ambientales de la DGT en trozos pequeños
que la web puede leer al momento.

Uso:
    python scripts/build_data.py <export_dist_ambiental.zip | fichero.txt> <carpeta_salida>

Formato de entrada (una línea por vehículo):  MATRICULA|CODIGO
    p. ej. 0003LWZ|16MC
Códigos DGT: ...0 = cero emisiones, ...E = ECO, ...C = C, ...B = B,
             "SIN DISTINTIVO" = sin etiqueta.

Salida:
  n/<LLL>.txt   matrículas actuales (0000LLL a 9999LLL): 10.000 caracteres,
                el carácter en la posición NNNN es la etiqueta de NNNNLLL.
  o/<KEY>.json  resto de matrículas (antiguas, ciclomotores...): {matricula: codigo}
  meta.json     fecha y recuento.
Códigos de salida: 0, E, C, B, N (sin distintivo), . (no aparece).
"""
import io
import json
import os
import re
import sys
import zipfile
from datetime import datetime, timezone

LETTERS = "BCDFGHJKLMNPRSTVWXYZ"
MODERN = re.compile(r"^(\d{4})([BCDFGHJKLMNPRSTVWXYZ]{3})$")
OLD = re.compile(r"^([A-Z]{1,3})(\d{2})")
SEP = re.compile(r"[|;,\t]")


def label_of(code: str) -> str:
    c = code.strip().upper()
    if not c or "SIN" in c:
        return "N"
    last = c[-1]
    if last in "0ECB":
        return last
    return "N"


def normalize(plate: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", plate.upper())


def other_key(plate: str) -> str:
    m = OLD.match(plate)
    if m:
        return m.group(1) + m.group(2)
    return "X" + plate[:3]


def open_lines(path: str):
    if path.lower().endswith(".zip"):
        zf = zipfile.ZipFile(path)
        names = [n for n in zf.namelist() if not n.endswith("/")]
        name = max(names, key=lambda n: zf.getinfo(n).file_size)
        raw = zf.open(name)
    else:
        raw = open(path, "rb")
    return io.TextIOWrapper(raw, encoding="latin-1", newline="")


def build(src: str, out: str) -> dict:
    modern: dict[str, bytearray] = {}
    others: dict[str, dict[str, str]] = {}
    counts = {"0": 0, "E": 0, "C": 0, "B": 0, "N": 0}
    total = skipped = 0
    for line in open_lines(src):
        parts = SEP.split(line.strip(), maxsplit=1)
        if len(parts) != 2:
            skipped += 1
            continue
        plate = normalize(parts[0])
        if not plate or plate.startswith("MATRICULA"):
            skipped += 1
            continue
        lab = label_of(parts[1])
        total += 1
        counts[lab] += 1
        m = MODERN.match(plate)
        if m:
            arr = modern.get(m.group(2))
            if arr is None:
                arr = modern[m.group(2)] = bytearray(b"." * 10000)
            arr[int(m.group(1))] = ord(lab)
        else:
            others.setdefault(other_key(plate), {})[plate] = lab

    if total < 1000 and not os.environ.get("ALLOW_SMALL"):
        raise SystemExit(f"Solo {total} matrículas leídas: el fichero de la DGT parece incorrecto")

    os.makedirs(os.path.join(out, "n"), exist_ok=True)
    os.makedirs(os.path.join(out, "o"), exist_ok=True)
    for key, arr in modern.items():
        with open(os.path.join(out, "n", key + ".txt"), "wb") as f:
            f.write(bytes(arr))
    for key, d in others.items():
        with open(os.path.join(out, "o", key + ".json"), "w") as f:
            json.dump(d, f, separators=(",", ":"))
    meta = {
        "actualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total": total,
        "por_etiqueta": counts,
        "descartadas": skipped,
        "trozos_actuales": len(modern),
        "trozos_otros": len(others),
    }
    with open(os.path.join(out, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return meta


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(json.dumps(build(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=1))
