# PigPlotter

Live geolocation plotting pipeline. A device `POST`s a point to a FastAPI endpoint; every
connected dashboard receives it immediately over a WebSocket and drops a marker on a
[MapLibre GL](https://maplibre.org/) map. Ships with an Android viewer that wraps the same
dashboard in a `WebView`.

## Layout

| Path | What it is |
| --- | --- |
| `app.py` | FastAPI service — dashboard HTML, ingest endpoint, WebSocket broadcast |
| `server/app.py` | Byte-identical copy of `app.py` used for deployment |
| `build_templates.py` | Generates the embedded dashboard HTML (reads `server/sound_b64.txt`) |
| `server/pigplotter_publisher.py` | Reusable publisher client + `--lat/--lon` CLI |
| `server/test_pipe.sh` | `curl` smoke test against an endpoint |
| `server/nginx_proxy_manager.conf` | Nginx Proxy Manager block with WebSocket upgrade headers |
| `app/` | Android app (Kotlin, `com.example.pigplotter`) |

## HTTP API

| Route | Purpose |
| --- | --- |
| `GET /` | The live dashboard (MapLibre GL map, dark theme, per-node popups) |
| `GET /points` | Snapshot of the last known point for every node |
| `POST /pipe` | Ingest a point: `{"id", "lat", "lon", ...any details}` |
| `WS /ws/stream` | Live push of each ingested point to connected dashboards |

## Run the server

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r server/requirements.txt
python3 app.py          # binds 0.0.0.0:8000
```

Then open <http://127.0.0.1:8000>.

## Send a point

```bash
curl -X POST http://127.0.0.1:8000/pipe \
  -H 'Content-Type: application/json' \
  -d '{"id":"orin-nano-01","lat":36.7378,"lon":-119.7871,"status":"Active","confidence":0.94}'
```

Or with the bundled client:

```bash
python3 server/pigplotter_publisher.py --lat 36.7378 --lon -119.7871 \
  --id orin-nano-01 --detail status=Active --detail confidence=0.94
# add --public to target https://pigplotter.duckdns.org/pipe instead of localhost
```

`--detail key=value` values are coerced to bool / int / float / JSON where possible.

## Android app

- Kotlin, `minSdk 24`, `targetSdk 37`, dependencies declared in `gradle/libs.versions.toml`.
- `MainActivity` hosts a `WebView` around the dashboard, grants geolocation to the page,
  and plays `res/raw/dart_throw.mp3` via `SoundPool`.
- Server URL is persisted in `SharedPreferences` under `server_url`, defaulting to
  `https://pigplotter.duckdns.org`.
- Requires `INTERNET` and location permissions.

```bash
./gradlew :app:assembleDebug
```

## Deployment notes

- The public demo endpoint is `https://pigplotter.duckdns.org`, fronted by Nginx Proxy
  Manager. WebSocket upgrade must be enabled — see `server/nginx_proxy_manager.conf`.
- `uvicorn` is started with `proxy_headers=True` and `forwarded_allow_ips="*"`.

## Caveats

- `app.py`, `server/app.py` and the generated HTML in `build_templates.py` are duplicated
  copies of the same code; edits have to be applied in more than one place.
- `build_templates.py` contains an absolute path (`/home/x/...`) and needs adjusting on
  another machine.
- The dashboard loads MapLibre from the unpkg CDN, so it requires internet access.
- CORS is currently `allow_origins=["*"]` — acceptable for a demo, tighten before
  relying on it.
