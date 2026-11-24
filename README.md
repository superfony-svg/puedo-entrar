# ¿Puedo entrar?

Web gratuita que, a partir de la matrícula, dice la etiqueta ambiental de la DGT de un vehículo y si puede entrar en las zonas de bajas emisiones (ZBE).

## Cómo funciona

- `web/`: la web (una sola página) y los datos de las zonas (`web/data/zonas.json`).
- `scripts/build_data.py`: convierte el fichero oficial de la DGT (`export_dist_ambiental.zip`, unos 30 millones de matrículas) en miles de trozos pequeños, para que la web solo descargue el que necesita.
- `.github/workflows/publicar.yml`: cada noche descarga el fichero de la DGT, prepara los datos y publica la web en GitHub Pages. También se ejecuta con cada cambio en `main` y a mano desde la pestaña *Actions*.

## Fuentes

- Etiquetas: Dirección General de Tráfico (Organismo Autónomo Jefatura Central de Tráfico), microdatos de distintivo ambiental. Se citan como fuente y no se alteran.
- Zonas: Punto de Acceso Nacional de la DGT (nap.dgt.es), licencia CC BY 4.0.
- Mapa: © OpenStreetMap.

Web no oficial e informativa.
