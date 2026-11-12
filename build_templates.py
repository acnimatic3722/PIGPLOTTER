#!/usr/bin/env python3
import os

with open("/home/x/AndroidStudioProjects/pigplotter/server/sound_b64.txt") as f:
    sound_b64 = f.read().strip()

map_html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>PigPlotter Live Stream</title>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
    <link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet" />
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; overflow: hidden; background: #0f172a; font-weight: 600; }}
        #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}

        /* Marker Popup Styling (Bold & Bigger) */
        .maplibregl-popup-content {{
            border-radius: 14px !important;
            padding: 14px 16px !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35) !important;
        }}
        .popup-content {{
            font-size: 15px;
            max-height: 280px;
            overflow-y: auto;
            line-height: 1.5;
            min-width: 210px;
            font-weight: 600;
        }}
        .popup-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #cbd5e1;
            padding-bottom: 5px;
            margin-bottom: 8px;
        }}
        .popup-title {{
            font-size: 18px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: 0.2px;
            margin: 0;
        }}
        .popup-age-badge {{
            font-size: 12px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
            white-space: nowrap;
        }}
        .popup-row {{
            margin-bottom: 4px;
            word-break: break-word;
            color: #1e293b;
            font-size: 14px;
            font-weight: 600;
        }}
        .popup-key {{
            font-weight: 800;
            color: #000000;
            font-size: 14px;
            margin-right: 4px;
        }}

        /* Clean Top Status Banner */
        .top-status-bar {{
            position: absolute;
            top: 12px;
            left: 12px;
            right: 12px;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.88);
            backdrop-filter: blur(12px);
            padding: 8px 14px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 4px 16px rgba(0,0,0,0.35);
        }}
        .status-group {{
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 0;
            cursor: pointer;
        }}
        .status-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #f59e0b;
            flex-shrink: 0;
            box-shadow: 0 0 10px #f59e0b;
            transition: all 0.3s;
        }}
        .status-dot.connected {{
            background: #10b981;
            box-shadow: 0 0 10px #10b981;
        }}
        .status-dot.error {{
            background: #ef4444;
            box-shadow: 0 0 10px #ef4444;
        }}
        .status-text {{
            font-size: 15px;
            font-weight: 800;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            letter-spacing: 0.3px;
            color: #f8fafc;
        }}
        .status-sub {{
            font-size: 12px;
            color: #cbd5e1;
            display: block;
            font-weight: 600;
        }}

        /* Bottom Controls Dock (Views & Actions at Bottom) */
        .bottom-dock {{
            position: absolute;
            bottom: 14px;
            left: 10px;
            right: 10px;
            z-index: 12;
            display: flex;
            flex-direction: column;
            gap: 8px;
            pointer-events: none;
        }}

        /* Bottom View Switcher Row */
        .bottom-view-bar {{
            pointer-events: auto;
            display: flex;
            justify-content: center;
            gap: 6px;
            background: rgba(15, 23, 42, 0.92);
            backdrop-filter: blur(14px);
            padding: 5px 8px;
            border-radius: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.45);
            border: 1px solid rgba(255,255,255,0.15);
            overflow-x: auto;
        }}
        .view-btn {{
            background: transparent;
            color: #cbd5e1;
            border: 1px solid transparent;
            border-radius: 20px;
            padding: 7px 13px;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s;
            user-select: none;
        }}
        .view-btn:active {{
            transform: scale(0.96);
        }}
        .view-btn.active {{
            background: #e63946;
            color: #ffffff;
            border-color: #ff5e6c;
            box-shadow: 0 2px 10px rgba(230, 57, 70, 0.45);
        }}

        /* Bottom Main Action Bar */
        .bottom-action-bar {{
            pointer-events: auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
            background: rgba(15, 23, 42, 0.94);
            backdrop-filter: blur(16px);
            padding: 8px 10px;
            border-radius: 16px;
            box-shadow: 0 6px 24px rgba(0,0,0,0.55);
            border: 1px solid rgba(255,255,255,0.18);
        }}
        .action-btn {{
            flex: 1;
            background: rgba(255,255,255,0.12);
            color: #f8fafc;
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 10px;
            padding: 9px 8px;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            text-align: center;
            white-space: nowrap;
            transition: all 0.15s, transform 0.1s;
            user-select: none;
            letter-spacing: 0.2px;
        }}
        .action-btn:active {{
            transform: scale(0.96);
        }}
        .action-btn.active {{
            background: #e63946;
            border-color: #e63946;
        }}
        .action-btn.highlight {{
            background: #e63946;
            border-color: #ff5e6c;
            box-shadow: 0 0 12px rgba(230, 57, 70, 0.5);
        }}
        .action-btn.sound-pulse {{
            animation: pulse-border 0.4s ease-out;
        }}

        @keyframes pulse-border {{
            0% {{ box-shadow: 0 0 0 0 rgba(230, 57, 70, 0.9); }}
            100% {{ box-shadow: 0 0 0 16px rgba(230, 57, 70, 0); }}
        }}

        /* Plot Points List Overlay Modal / Drawer (Anchored Above Bottom Dock) */
        .points-overlay {{
            position: absolute;
            bottom: 116px;
            left: 10px;
            right: 10px;
            max-height: calc(100vh - 180px);
            background: rgba(15, 23, 42, 0.96);
            backdrop-filter: blur(18px);
            color: #f8fafc;
            border-radius: 18px;
            z-index: 20;
            padding: 16px;
            display: none;
            flex-direction: column;
            box-shadow: 0 16px 40px rgba(0,0,0,0.7);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .points-overlay.open {{
            display: flex;
        }}
        .overlay-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.15);
            margin-bottom: 12px;
        }}
        .overlay-title {{
            font-size: 17px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: 0.2px;
        }}
        .overlay-search {{
            width: 100%;
            background: #0f172a;
            border: 1px solid #475569;
            color: #f8fafc;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 14.5px;
            font-weight: 600;
            margin-bottom: 12px;
            outline: none;
        }}
        .overlay-search:focus {{
            border-color: #e63946;
            box-shadow: 0 0 8px rgba(230, 57, 70, 0.35);
        }}
        .points-scroll-list {{
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding-right: 4px;
            max-height: calc(100vh - 270px);
        }}
        .point-card {{
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px;
            padding: 12px 14px;
            cursor: pointer;
            transition: background 0.15s, border-color 0.15s;
        }}
        .point-card:hover, .point-card:active {{
            background: rgba(51, 65, 85, 0.95);
            border-color: #e63946;
        }}
        .point-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}
        .point-card-id {{
            font-size: 16px;
            font-weight: 800;
            color: #f8fafc;
            letter-spacing: 0.3px;
        }}
        .point-card-coords {{
            font-size: 13.5px;
            color: #cbd5e1;
            font-family: ui-monospace, monospace;
            font-weight: 700;
        }}
        .point-card-details {{
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed rgba(255,255,255,0.16);
            font-size: 14px;
            font-weight: 600;
            line-height: 1.6;
            color: #e2e8f0;
            display: none;
        }}
        .point-card-details.expanded {{
            display: block;
        }}
        .detail-badge {{
            display: inline-block;
            border-radius: 7px;
            padding: 3px 8px;
            font-size: 13px;
            font-weight: 700;
        }}
        .point-actions {{
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }}
        .point-action-btn {{
            background: rgba(255,255,255,0.12);
            color: #f8fafc;
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.15s;
        }}
        .point-action-btn:hover, .point-action-btn:active {{
            background: #e63946;
            border-color: #e63946;
        }}

        /* Standard Modals (Bold & Bigger) */
        .modal-backdrop {{
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,0.7);
            z-index: 30;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }}
        .modal-backdrop.open {{ display: flex; }}
        .modal {{
            background: #1e293b;
            color: #f8fafc;
            width: 100%;
            max-width: 400px;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 12px 36px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.16);
        }}
        .modal h4 {{
            margin: 0 0 14px 0;
            font-size: 17px;
            font-weight: 800;
            letter-spacing: 0.2px;
        }}
        .modal label {{
            display: block;
            font-size: 14px;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 6px;
        }}
        .modal input, .modal textarea, .modal select {{
            width: 100%;
            background: #0f172a;
            border: 1px solid #475569;
            color: #f8fafc;
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
            font-family: inherit;
        }}
        .modal-actions {{
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 8px;
        }}
    </style>
</head>
<body>
    <!-- Top Status Bar -->
    <div class="top-status-bar">
        <div class="status-group" onclick="togglePointsOverlay()">
            <div id="statusDot" class="status-dot"></div>
            <div>
                <div class="status-text" id="statusTitle">PigPlotter Live</div>
                <span class="status-sub" id="statusSub">Connecting...</span>
            </div>
        </div>
        <div style="font-size:12px;color:#94a3b8;font-weight:700;" id="connectionMeta">MapTiler • OSM</div>
    </div>

    <!-- Plot Points List Overlay (Slides up above bottom controls) -->
    <div id="pointsOverlay" class="points-overlay">
        <div class="overlay-header">
            <div class="overlay-title">
                <span>📍 Plot Points</span>
                <span id="overlayBadge" class="detail-badge" style="background:rgba(230,57,70,0.25);color:#ff5e6c;border:1px solid rgba(230,57,70,0.4);">0 points</span>
            </div>
            <button class="action-btn" style="flex:none;padding:5px 12px;" onclick="togglePointsOverlay()">✕ Close</button>
        </div>
        <input id="pointsSearchInput" class="overlay-search" type="text" placeholder="🔍 Search by ID or details..." oninput="renderPointsList()" />
        <div id="pointsListContainer" class="points-scroll-list">
            <div style="font-size:14px;color:#94a3b8;padding:20px 0;text-align:center;font-weight:600;">
                No plot points on map yet.<br/>Waiting for pipeline telemetry...
            </div>
        </div>
    </div>

    <!-- Bottom Controls Dock (View Bar + Action Bar) -->
    <div class="bottom-dock">
        <!-- View Switcher Bar at Bottom -->
        <div class="bottom-view-bar">
            <button id="viewBtn-satellite" class="view-btn active" onclick="setMapStyle('satellite')">🛰️ Satellite</button>
            <button id="viewBtn-streets" class="view-btn" onclick="setMapStyle('streets')">🗺️ Streets</button>
            <button id="viewBtn-outdoor" class="view-btn" onclick="setMapStyle('outdoor')">⛰️ Terrain</button>
            <button id="viewBtn-dark" class="view-btn" onclick="setMapStyle('dark')">🌙 Dark</button>
        </div>

        <!-- Main Actions Bar at Bottom -->
        <div class="bottom-action-bar">
            <button id="btnPoints" class="action-btn highlight" onclick="togglePointsOverlay()">📍 Points (0)</button>
            <button id="btnFollow" class="action-btn active" onclick="toggleFollow()">🎯 Follow</button>
            <button class="action-btn" onclick="openPipeModal()">➕ Pipe</button>
            <button class="action-btn" style="flex:0.6;" onclick="openSettingsModal()">⚙</button>
        </div>
    </div>

    <!-- Settings Modal -->
    <div id="settingsModal" class="modal-backdrop">
        <div class="modal">
            <h4>Pipeline &amp; Display Settings</h4>
            <label>Map Style (MapTiler)</label>
            <select id="mapStyleSelect">
                <option value="satellite">🛰️ Satellite Hybrid (MapTiler)</option>
                <option value="streets">🗺️ Streets v2 (MapTiler)</option>
                <option value="outdoor">⛰️ Terrain / Outdoor (MapTiler)</option>
                <option value="dark">🌙 Dark Mode (MapTiler)</option>
            </select>
            <label>Base Server URL (HTTPS / HTTP)</label>
            <input id="serverUrlInput" type="text" placeholder="https://pigplotter.duckdns.org" />
            <div class="modal-actions">
                <button class="action-btn" style="flex:none;padding:8px 14px;" onclick="closeModals()">Cancel</button>
                <button class="action-btn active" style="flex:none;padding:8px 14px;" onclick="saveServerUrl()">Save Settings</button>
            </div>
        </div>
    </div>

    <!-- Push Pipe Payload Modal -->
    <div id="pipeModal" class="modal-backdrop">
        <div class="modal">
            <h4>Push Plot Point to /pipe</h4>
            <label>JSON Payload</label>
            <textarea id="pipePayloadInput" rows="7">{{
  "id": "orin-nano-01",
  "lat": 36.7378,
  "lon": -119.7871,
  "status": "Active",
  "confidence": 0.94,
  "notes": "Live plot point via NPM"
}}</textarea>
            <div class="modal-actions">
                <button class="action-btn" style="flex:none;padding:8px 12px;" onclick="fillDeviceGps()">Use Phone GPS</button>
                <button class="action-btn" style="flex:none;padding:8px 12px;" onclick="closeModals()">Cancel</button>
                <button class="action-btn active" style="flex:none;padding:8px 12px;" onclick="sendPipePayload()">POST /pipe</button>
            </div>
        </div>
    </div>

    <div id="map"></div>

    <script>
        const DEFAULT_BASE_URL = "https://pigplotter.duckdns.org";
        const MAPTILER_KEY = "y1BVVGaTua5i22ceEgRF";

        // Pin aging steps (Matches backend: Red -> Amber -> Gray)
        const PIN_AGE_STEPS = [
            {{ maxAge: 2 * 60, color: '#e63946', label: 'Fresh (<2m)' }},
            {{ maxAge: 10 * 60, color: '#f59e0b', label: 'Recent (<10m)' }},
            {{ maxAge: Infinity, color: '#6b7280', label: 'Older (>10m)' }}
        ];

        function pinColor(ts) {{
            if (!ts) return '#e63946';
            const age = Math.max(0, (Date.now() / 1000) - ts);
            for (const step of PIN_AGE_STEPS) {{
                if (age < step.maxAge) return step.color;
            }}
            return '#6b7280';
        }}

        function applyPinColor(marker, ts) {{
            if (!marker) return;
            const el = marker.getElement();
            if (!el) return;
            const path = el.querySelector('path');
            if (path) {{
                path.setAttribute('fill', pinColor(ts));
            }}
        }}

        function formatAge(ts) {{
            if (!ts) return "Just now";
            const sec = Math.max(0, Math.floor((Date.now() / 1000) - ts));
            if (sec < 60) return `${{sec}}s ago`;
            const min = Math.floor(sec / 60);
            if (min < 60) return `${{min}}m ago`;
            const hr = Math.floor(min / 60);
            if (hr < 24) return `${{hr}}h ago`;
            const days = Math.floor(hr / 24);
            return `${{days}}d ago`;
        }}

        // Dart throw audio
        const DART_SOUND_B64 = "data:audio/mp3;base64,{sound_b64}";
        let dartAudio = null;
        try {{
            dartAudio = new Audio(DART_SOUND_B64);
            dartAudio.preload = "auto";
        }} catch(e) {{
            console.warn("HTML5 audio setup:", e);
        }}

        function playDartSound() {{
            if (window.AndroidBridge && window.AndroidBridge.playPlotSound) {{
                try {{
                    window.AndroidBridge.playPlotSound();
                    return;
                }} catch (e) {{}}
            }}
            if (dartAudio) {{
                try {{
                    dartAudio.currentTime = 0;
                    dartAudio.play().catch(e => console.log("Audio play notice:", e));
                }} catch (e) {{}}
            }}
        }}

        function getBaseUrl() {{
            if (window.AndroidBridge && window.AndroidBridge.getServerUrl) {{
                return window.AndroidBridge.getServerUrl() || DEFAULT_BASE_URL;
            }}
            return localStorage.getItem("pigplotter_base_url") || DEFAULT_BASE_URL;
        }}

        const MAP_STYLES = {{
            satellite: {{
                name: "🛰️ Satellite",
                url: `https://api.maptiler.com/maps/hybrid/style.json?key=${{MAPTILER_KEY}}`
            }},
            streets: {{
                name: "🗺️ Streets",
                url: `https://api.maptiler.com/maps/streets-v2/style.json?key=${{MAPTILER_KEY}}`
            }},
            outdoor: {{
                name: "⛰️ Terrain",
                url: `https://api.maptiler.com/maps/outdoor-v2/style.json?key=${{MAPTILER_KEY}}`
            }},
            dark: {{
                name: "🌙 Dark",
                url: `https://api.maptiler.com/maps/dataviz-dark/style.json?key=${{MAPTILER_KEY}}`
            }}
        }};

        let currentStyleKey = localStorage.getItem("pigplotter_map_style") || "satellite";

        const map = new maplibregl.Map({{
            container: 'map',
            style: MAP_STYLES[currentStyleKey].url,
            center: [-119.7871, 36.7378],
            zoom: 13
        }});

        map.addControl(new maplibregl.NavigationControl(), 'top-right');

        // Markers dictionary stores: {{ marker, ts }}
        const mapMarkers = {{}};
        const latestPayloads = {{}};
        const expandedCards = new Set();
        let autoFollow = true;
        let activeSocket = null;
        let reconnectTimer = null;

        function refreshPinAges() {{
            for (const entry of Object.values(mapMarkers)) {{
                if (entry && entry.marker && entry.ts) {{
                    applyPinColor(entry.marker, entry.ts);
                }}
            }}
            renderPointsList();
        }}

        // Periodically refresh pin ages every 10 seconds
        setInterval(refreshPinAges, 10000);

        function setMapStyle(key) {{
            if (!MAP_STYLES[key]) key = "satellite";
            currentStyleKey = key;
            localStorage.setItem("pigplotter_map_style", key);
            map.setStyle(MAP_STYLES[key].url);

            // Re-apply pin colors after style reload
            map.once('style.load', () => {{
                refreshPinAges();
            }});

            document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
            const activeBtn = document.getElementById('viewBtn-' + key);
            if (activeBtn) activeBtn.classList.add('active');

            const sel = document.getElementById("mapStyleSelect");
            if (sel) sel.value = key;
        }}

        function escapeHtml(str) {{
            return String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;");
        }}

        function generateDetailsHtml(id, payload, ts) {{
            const ageColor = pinColor(ts);
            const ageText = formatAge(ts);

            let html = `<div class="popup-content">
                <div class="popup-header">
                    <span class="popup-title">${{escapeHtml(id)}}</span>
                    <span class="popup-age-badge" style="background:${{ageColor}}25;color:${{ageColor}};border:1px solid ${{ageColor}}50;">${{ageText}}</span>
                </div>`;
            for (const [key, value] of Object.entries(payload || {{}})) {{
                if (key === 'ts') continue;
                const formattedVal = (typeof value === 'object' && value !== null)
                    ? JSON.stringify(value)
                    : value;
                html += `<div class="popup-row"><span class="popup-key">${{escapeHtml(key)}}:</span> ${{escapeHtml(formattedVal)}}</div>`;
            }}
            html += '</div>';
            return html;
        }}

        function upsertMarker(msg, panTo = true) {{
            if (!msg || msg.lat === undefined || msg.lon === undefined) return;
            const marker_id = String(msg.marker_id || "node_default");
            const lat = Number(msg.lat);
            const lon = Number(msg.lon);
            const full_payload = msg.full_payload || msg;
            const ts = Number(msg.ts) || Number(full_payload?.ts) || (Date.now() / 1000);

            if (Number.isNaN(lat) || Number.isNaN(lon)) return;

            // Trigger dart throw sound
            playDartSound();

            // Flash bottom action button
            const btnPoints = document.getElementById("btnPoints");
            if (btnPoints) {{
                btnPoints.classList.remove("sound-pulse");
                void btnPoints.offsetWidth;
                btnPoints.classList.add("sound-pulse");
            }}

            const htmlDetails = generateDetailsHtml(marker_id, full_payload, ts);
            latestPayloads[marker_id] = {{ marker_id, lat, lon, ts, full_payload }};

            let entry = mapMarkers[marker_id];
            if (entry) {{
                entry.marker.setLngLat([lon, lat]);
                entry.marker.getPopup().setHTML(htmlDetails);
                entry.ts = ts;
            }} else {{
                const popup = new maplibregl.Popup({{ offset: 25 }}).setHTML(htmlDetails);
                const marker = new maplibregl.Marker({{ color: pinColor(ts) }})
                    .setLngLat([lon, lat])
                    .setPopup(popup)
                    .addTo(map);
                entry = {{ marker, ts }};
                mapMarkers[marker_id] = entry;
            }}

            applyPinColor(entry.marker, entry.ts);

            if (panTo && autoFollow) {{
                map.flyTo({{ center: [lon, lat], speed: 0.9 }});
            }}

            renderPointsList();
        }}

        function togglePointsOverlay() {{
            const overlay = document.getElementById("pointsOverlay");
            overlay.classList.toggle("open");
            if (overlay.classList.contains("open")) {{
                renderPointsList();
            }}
        }}

        function toggleCardDetails(event, id) {{
            event.stopPropagation();
            if (expandedCards.has(id)) {{
                expandedCards.delete(id);
            }} else {{
                expandedCards.add(id);
            }}
            renderPointsList();
        }}

        function focusPoint(id) {{
            const item = latestPayloads[id];
            if (!item) return;

            map.flyTo({{
                center: [item.lon, item.lat],
                zoom: Math.max(map.getZoom(), 15),
                speed: 1.2
            }});

            const entry = mapMarkers[id];
            if (entry && entry.marker) {{
                if (!entry.marker.getPopup().isOpen()) {{
                    entry.marker.togglePopup();
                }}
            }}

            expandedCards.add(id);
            renderPointsList();

            if (window.innerWidth < 640) {{
                document.getElementById("pointsOverlay").classList.remove("open");
            }}
        }}

        function renderPointsList() {{
            const ids = Object.keys(latestPayloads);
            const totalCount = ids.length;

            const btnPoints = document.getElementById("btnPoints");
            if (btnPoints) btnPoints.textContent = `📍 Points (${{totalCount}})`;

            const badge = document.getElementById("overlayBadge");
            if (badge) badge.textContent = `${{totalCount}} points`;

            const search = (document.getElementById("pointsSearchInput")?.value || "").toLowerCase().trim();
            const container = document.getElementById("pointsListContainer");
            if (!container) return;

            if (totalCount === 0) {{
                container.innerHTML = `<div style="font-size:14px;color:#94a3b8;padding:20px 0;text-align:center;font-weight:600;">
                    No plot points received yet.<br/>Push to <code>/pipe</code> to see points appear here!
                </div>`;
                return;
            }}

            const filteredIds = ids.filter(id => {{
                if (!search) return true;
                if (id.toLowerCase().includes(search)) return true;
                const pl = latestPayloads[id].full_payload;
                return JSON.stringify(pl).toLowerCase().includes(search);
            }});

            if (filteredIds.length === 0) {{
                container.innerHTML = `<div style="font-size:14px;color:#94a3b8;padding:16px 0;text-align:center;font-weight:600;">
                    No plot points match "<strong>${{escapeHtml(search)}}</strong>"
                </div>`;
                return;
            }}

            container.innerHTML = filteredIds.map(id => {{
                const item = latestPayloads[id];
                const isExpanded = expandedCards.has(id);
                const payload = item.full_payload || {{}};
                const ageColor = pinColor(item.ts);
                const ageText = formatAge(item.ts);

                let detailsRows = "";
                for (const [k, v] of Object.entries(payload)) {{
                    const val = (typeof v === 'object' && v !== null) ? JSON.stringify(v) : v;
                    detailsRows += `<div style="margin-bottom:5px;word-break:break-word;font-size:14px;">
                        <strong style="color:#ffffff;font-weight:800;">${{escapeHtml(k)}}:</strong> <span style="color:#e2e8f0;font-weight:600;">${{escapeHtml(val)}}</span>
                    </div>`;
                }}

                return `
                <div class="point-card" onclick="focusPoint('${{escapeHtml(id)}}')">
                    <div class="point-card-top">
                        <span class="point-card-id" style="display:flex;align-items:center;gap:6px;">
                            <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${{ageColor}};box-shadow:0 0 8px ${{ageColor}};"></span>
                            ${{escapeHtml(id)}}
                        </span>
                        <span class="detail-badge" style="background:${{ageColor}}25;color:${{ageColor}};border:1px solid ${{ageColor}}50;">
                            ${{ageText}}
                        </span>
                    </div>
                    <div class="point-card-coords">${{item.lat.toFixed(5)}}, ${{item.lon.toFixed(5)}}</div>
                    <div class="point-actions">
                        <button class="point-action-btn" onclick="focusPoint('${{escapeHtml(id)}}')">🎯 Focus Pin</button>
                        <button class="point-action-btn" onclick="toggleCardDetails(event, '${{escapeHtml(id)}}')">
                            ${{isExpanded ? '▲ Hide Details' : '▼ Show Details'}}
                        </button>
                    </div>
                    <div class="point-card-details ${{isExpanded ? 'expanded' : ''}}">
                        ${{detailsRows}}
                    </div>
                </div>`;
            }}).join("");
        }}

        function setStatus(state, subtitle) {{
            const dot = document.getElementById("statusDot");
            const sub = document.getElementById("statusSub");
            if (dot) dot.className = "status-dot " + (state || "");
            if (sub) sub.textContent = subtitle;
        }}

        function buildWsUrl(baseUrl) {{
            const trimmed = baseUrl.trim().replace(/\\/+$/, "");
            if (trimmed.startsWith("wss://") || trimmed.startsWith("ws://")) {{
                return trimmed.endsWith("/ws/stream") ? trimmed : (trimmed + "/ws/stream");
            }}
            if (trimmed.startsWith("https://")) {{
                return "wss://" + trimmed.slice("https://".length) + "/ws/stream";
            }}
            if (trimmed.startsWith("http://")) {{
                return "ws://" + trimmed.slice("http://".length) + "/ws/stream";
            }}
            return "wss://" + trimmed + "/ws/stream";
        }}

        function connectWebSocket() {{
            if (reconnectTimer) {{
                clearTimeout(reconnectTimer);
                reconnectTimer = null;
            }}
            if (activeSocket) {{
                try {{ activeSocket.onclose = null; activeSocket.close(); }} catch (e) {{}}
            }}

            const baseUrl = getBaseUrl();
            const wsUrl = buildWsUrl(baseUrl);
            setStatus("", `Connecting: ${{wsUrl}}`);

            try {{
                const ws = new WebSocket(wsUrl);
                activeSocket = ws;

                ws.onopen = function() {{
                    setStatus("connected", `Live: ${{baseUrl.replace(/^https?:\\/\\//, '')}}`);
                }};

                ws.onmessage = function(event) {{
                    try {{
                        const msg = JSON.parse(event.data);
                        if (msg.type === 'initial_state' && msg.points) {{
                            const pts = Object.values(msg.points);
                            pts.forEach(pt => upsertMarker(pt, false));
                            if (pts.length > 0 && autoFollow) {{
                                const last = pts[pts.length - 1];
                                map.flyTo({{ center: [ Number(last.lon), Number(last.lat) ], speed: 0.9 }});
                            }}
                        }} else {{
                            upsertMarker(msg, true);
                        }}
                    }} catch (err) {{
                        console.error("Invalid WS packet:", err);
                    }}
                }};

                ws.onerror = function() {{
                    setStatus("error", "Stream error - retrying...");
                }};

                ws.onclose = function() {{
                    setStatus("", "Disconnected - reconnecting in 2s...");
                    reconnectTimer = setTimeout(connectWebSocket, 2000);
                }};
            }} catch (err) {{
                setStatus("error", "Invalid WebSocket URL");
                reconnectTimer = setTimeout(connectWebSocket, 3000);
            }}
        }}

        function toggleFollow() {{
            autoFollow = !autoFollow;
            const btn = document.getElementById("btnFollow");
            if (btn) btn.classList.toggle("active", autoFollow);
        }}

        function openSettingsModal() {{
            document.getElementById("serverUrlInput").value = getBaseUrl();
            const sel = document.getElementById("mapStyleSelect");
            if (sel) sel.value = currentStyleKey;
            document.getElementById("settingsModal").classList.add("open");
        }}

        function openPipeModal() {{
            document.getElementById("pipeModal").classList.add("open");
        }}

        function closeModals() {{
            document.getElementById("settingsModal").classList.remove("open");
            document.getElementById("pipeModal").classList.remove("open");
        }}

        function saveServerUrl() {{
            const val = document.getElementById("serverUrlInput").value.trim() || DEFAULT_BASE_URL;
            localStorage.setItem("pigplotter_base_url", val);
            if (window.AndroidBridge && window.AndroidBridge.setServerUrl) {{
                window.AndroidBridge.setServerUrl(val);
            }}
            const sel = document.getElementById("mapStyleSelect");
            if (sel && sel.value !== currentStyleKey) {{
                setMapStyle(sel.value);
            }}
            closeModals();
            connectWebSocket();
        }}

        function fillDeviceGps() {{
            if (window.AndroidBridge && window.AndroidBridge.requestDeviceLocation) {{
                window.AndroidBridge.requestDeviceLocation();
            }} else if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(pos => {{
                    onDeviceLocation(pos.coords.latitude, pos.coords.longitude);
                }});
            }}
        }}

        window.onDeviceLocation = function(lat, lon) {{
            try {{
                const current = JSON.parse(document.getElementById("pipePayloadInput").value);
                current.lat = Number(lat.toFixed(6));
                current.lon = Number(lon.toFixed(6));
                document.getElementById("pipePayloadInput").value = JSON.stringify(current, null, 2);
            }} catch (e) {{
                document.getElementById("pipePayloadInput").value = JSON.stringify({{
                    id: "android-mobile-01",
                    lat: Number(lat.toFixed(6)),
                    lon: Number(lon.toFixed(6)),
                    status: "Active",
                    notes: "Live GPS from Android"
                }}, null, 2);
            }}
        }};

        async function sendPipePayload() {{
            const raw = document.getElementById("pipePayloadInput").value;
            let parsed;
            try {{
                parsed = JSON.parse(raw);
            }} catch (e) {{
                alert("Invalid JSON payload");
                return;
            }}
            const baseUrl = getBaseUrl().replace(/\\/+$/, "");
            const pipeUrl = baseUrl + "/pipe";

            if (window.AndroidBridge && window.AndroidBridge.postToPipe) {{
                window.AndroidBridge.postToPipe(pipeUrl, JSON.stringify(parsed));
                closeModals();
                return;
            }}

            try {{
                await fetch(pipeUrl, {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify(parsed)
                }});
                closeModals();
            }} catch (e) {{
                alert("POST /pipe failed: " + e.message);
            }}
        }}

        setMapStyle(currentStyleKey);
        connectWebSocket();
    </script>
</body>
</html>
'''

with open("/home/x/AndroidStudioProjects/pigplotter/app/src/main/assets/map.html", "w") as f:
    f.write(map_html_content)

server_app_content = f'''import json
import time
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="PigPlotter Live Stream Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_dashboards = set()
latest_points = {{}}

HTML_TEMPLATE = """{map_html_content}"""

@app.get("/")
async def serve_map_dashboard():
    return HTMLResponse(HTML_TEMPLATE)

@app.get("/points")
async def get_latest_points():
    return {{"type": "initial_state", "points": latest_points}}

@app.websocket("/ws/stream")
async def websocket_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_dashboards.add(websocket)
    try:
        if latest_points:
            await websocket.send_text(json.dumps({{
                "type": "initial_state",
                "points": latest_points
            }}))
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_dashboards.discard(websocket)
    except Exception:
        connected_dashboards.discard(websocket)

@app.post("/pipe")
async def inbound_pipeline_receiver(request: Request):
    try:
        payload = await request.json()
    except Exception:
        return {{"status": "error", "message": "Invalid JSON format"}}

    lat = payload.get("lat") if payload.get("lat") is not None else payload.get("latitude")
    lon = payload.get("lon") if payload.get("lon") is not None else (
        payload.get("lng") if payload.get("lng") is not None else payload.get("longitude")
    )
    marker_id = str(payload.get("id") or payload.get("tid") or payload.get("device_id") or "node_default")

    if lat is None or lon is None:
        return {{"status": "skipped", "message": "Missing coordinate values (lat/lon)"}}

    raw_ts = payload.get("ts")
    if raw_ts is None:
        ts = time.time()
    else:
        try:
            ts = float(raw_ts)
            if ts > 1e11:  # milliseconds
                ts = ts / 1000.0
        except Exception:
            ts = time.time()

    broadcast_packet = {{
        "marker_id": marker_id,
        "lat": float(lat),
        "lon": float(lon),
        "ts": ts,
        "full_payload": payload
    }}

    latest_points[marker_id] = broadcast_packet

    disconnected_clients = set()
    for client in connected_dashboards:
        try:
            await client.send_text(json.dumps(broadcast_packet))
        except Exception:
            disconnected_clients.add(client)

    for dead_client in disconnected_clients:
        connected_dashboards.discard(dead_client)

    return {{"status": "dispatched", "targets_notified": len(connected_dashboards)}}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )
'''

with open("/home/x/AndroidStudioProjects/pigplotter/server/app.py", "w") as f:
    f.write(server_app_content)

with open("/home/x/AndroidStudioProjects/pigplotter/app.py", "w") as f:
    f.write(server_app_content)

print("Generated pin aging updates successfully!")
