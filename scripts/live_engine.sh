#!/bin/bash

BASE="$(cd "$(dirname "$0")/.." && pwd)"

echo "=========================================="
echo "       3D GOKIL LIVE ENGINE"
echo "=========================================="
echo "Base: $BASE"
echo "LIVE engine tahap 1"
echo "FFmpeg + YouTube belum disambungkan."

trap 'echo "3D GOKIL LIVE STOP"; exit 0' TERM INT

while true; do
    sleep 5
done
