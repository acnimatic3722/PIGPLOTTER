#!/usr/bin/env python3
"""
PigPlotter Publisher Client for Jetson Orin Nano
Use as a reusable Python library or as a standalone CLI tool to send telemetry
and plot points to the PigPlotter live stream pipeline.
"""

import argparse
import json
import sys
from typing import Any, Dict, Optional
import requests

DEFAULT_ENDPOINT = "http://127.0.0.1:8000/pipe"
DEFAULT_PUBLIC_ENDPOINT = "https://pigplotter.duckdns.org/pipe"


def send_plot_point(
    lat: float,
    lon: float,
    node_id: str = "orin-nano-01",
    endpoint: str = DEFAULT_ENDPOINT,
    timeout: float = 5.0,
    **details: Any
) -> Dict[str, Any]:
    """
    Publish a plot point with arbitrary details to the PigPlotter pipeline.

    :param lat: Latitude as float
    :param lon: Longitude as float
    :param node_id: Unique identifier for this device/node
    :param endpoint: Target URL (defaults to local pipeline http://127.0.0.1:8000/pipe)
    :param timeout: HTTP request timeout in seconds
    :param details: Key-value metadata attached to this plot point
    :return: Response dict from server
    """
    payload: Dict[str, Any] = {
        "id": node_id,
        "lat": float(lat),
        "lon": float(lon),
        **details
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[PigPlotter Error] Failed to publish to {endpoint}: {e}", file=sys.stderr)
        return {"status": "error", "message": str(e)}


def parse_detail_arg(arg: str) -> tuple:
    """Parse 'key=value' string into key and converted value."""
    if "=" not in arg:
        return arg, True
    k, v = arg.split("=", 1)
    k = k.strip()
    v = v.strip()
    # Try parsing number or boolean or JSON if possible
    if v.lower() == "true":
        return k, True
    if v.lower() == "false":
        return k, False
    try:
        if "." in v:
            return k, float(v)
        return k, int(v)
    except ValueError:
        pass
    try:
        return k, json.loads(v)
    except Exception:
        return k, v


def main():
    parser = argparse.ArgumentParser(description="Publish plot point to PigPlotter pipeline")
    parser.add_argument("--id", default="orin-nano-01", help="Device/node ID")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help=f"Pipeline endpoint (default: {DEFAULT_ENDPOINT})")
    parser.add_argument("--detail", "-d", action="append", default=[], help="Metadata key=value (e.g. status=Active)")
    parser.add_argument("--public", action="store_true", help="Send to public duckdns endpoint instead of localhost")

    args = parser.parse_args()

    endpoint = DEFAULT_PUBLIC_ENDPOINT if args.public else args.endpoint
    extra_details = {}
    for d in args.detail:
        k, v = parse_detail_arg(d)
        extra_details[k] = v

    print(f"Publishing to {endpoint} for node '{args.id}' @ ({args.lat}, {args.lon})...")
    res = send_plot_point(
        lat=args.lat,
        lon=args.lon,
        node_id=args.id,
        endpoint=endpoint,
        **extra_details
    )
    print("Response:", json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
