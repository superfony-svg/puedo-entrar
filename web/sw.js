// Permite instalar la web como app y abrirla sin conexión con lo último que se vio.
// Siempre intenta la red primero, así los datos están al día.
const CACHE = "puedo-entrar-v1";
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(["./", "./manifest.webmanifest", "./icons/icon-192.png"])).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const propio = url.origin === location.origin;
  const libreria = url.hostname === "cdnjs.cloudflare.com";
  if (!propio && !libreria) return; // el mapa (OpenStreetMap) va siempre por red
  e.respondWith(fetch(req).then(res => {
    if (res.ok) { const copia = res.clone(); caches.open(CACHE).then(c => c.put(req, copia)); }
    return res;
  }).catch(() => caches.match(req, {ignoreSearch: true}).then(r => r || caches.match("./"))));
});
