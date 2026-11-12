#!/usr/bin/env bash
# Jetson Orin Nano -> Outbound test payload to pigplotter.duckdns.org via Nginx Proxy Manager (HTTPS)
ENDPOINT="${1:-https://pigplotter.duckdns.org/pipe}"

curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "orin-nano-01",
    "lat": 36.7378,
    "lon": -119.7871,
    "status": "Active",
    "confidence": 0.94,
    "notes": "Live plot point via NPM"
  }'
echo ""
