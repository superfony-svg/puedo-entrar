# ¿Puedo entrar?

Web gratuita que, a partir de la matrícula, dice la etiqueta ambiental de la DGT de un vehículo y si puede entrar en las zonas de bajas emisiones (ZBE).

## Cómo funciona

- `web/`: la web (una sola página) y los datos de las zonas (`web/data/zonas.json`).
- `scripts/build_data.py`: convierte el fichero oficial de la DGT (`export_dist_ambiental.zip`, unos 30 millones de matrículas) en miles de trozos pequeños, para que la web solo descargue el que necesita.
- `.github/workflows/publicar.yml`: cada noche descarga el fichero de la DGT, prepara los datos y publica la web en GitHub Pages. También se ejecuta con cada cambio en `main` y a mano desde la pestaña *Actions*.

## Ficheros que se editan a mano (en `scripts/`)

- `correcciones.json`: corrige datos de la DGT por id de zona (por ejemplo, `permitidas`).
- `excepciones.json`: norma de cada ciudad para históricos (`historicos`), movilidad reducida (`pmr`), excepción para coches de vecinos (`residentes`, opcional: la web la aplica si el usuario dice que su coche paga el impuesto de circulación en esa ciudad), facilidades para visitantes (`visitantes`, opcional: sale en la página «Ciudades más abiertas»), `fuente` y `revisado`. Clave: nombre de la ciudad.
- `osm_zonas.json`: zonas de OpenStreetMap para ciudades que la DGT no publica.
- `avisos.json`: avisos por ciudad que cambian lo de la DGT (`aviso`, `fuente`, `estado`; un `estado` distinto de `active` hace que la web diga que se puede entrar). Ejemplo: Málaga, zona anulada.
- `manuales.json`: zonas puestas a mano para ciudades que no están ni en la DGT ni en OpenStreetMap (ejemplo: Almería). Sin contorno: `bbox` aproximado solo para centrar el mapa.
- `municipios.json`: lista de municipios y territorios insulares obligados a tener ZBE. Los que no tienen datos salen con una página básica (estado según prensa) y en `web/data/pendientes.json`.
- `guias.py`: texto de las guías (`web/guias/`).

`scripts/build_paginas.py` genera las páginas de ciudad, las guías, la clasificación `web/ciudades-abiertas/`, el mapa del sitio y aplica `avisos.json`.

## Fuentes

- Etiquetas: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico), microdatos de distintivo ambiental. Se citan como fuente y no se alteran.
- Zonas: Punto de Acceso Nacional de la DGT (nap.dgt.es), licencia CC BY 4.0.
- Mapa: © OpenStreetMap.

Web no oficial e informativa.

## Aparcamientos disuasorios

`scripts/build_parkings.py` pide a OpenStreetMap, en una sola consulta para toda España, los aparcamientos con la etiqueta `park_ride` y asigna a cada ciudad los que quedan a unos 6 km de sus zonas. Escribe `web/data/parkings.json` (`{"Ciudad": [{"n", "lat", "lon", "pago", "plazas", "tipo"}]}`). Si Overpass no responde usa la copia guardada en `osm_cache/pr_espana.json`. Cada página de ciudad los muestra en «Si tu coche no puede entrar», junto con el permiso de visitantes de `excepciones.json` (campo `visitantes`).
