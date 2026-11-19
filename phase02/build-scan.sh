#!/bin/bash
# Build the updater image and scan both containers for vulnerabilities with Trivy.
# Usage: ./scan.sh          (uses tag 01)
#        TAG=02 ./scan.sh   (uses another tag)

# This will stop the script if the build fails.
set -euo pipefail

TAG="${TAG:-01}"

# Run from this script's folder so the Docker build finds the Dockerfile.
cd "$(dirname "$0")"

#echo "====> Building updater:$TAG <===="
#docker build -t "updater:$TAG" .

echo "====> Scanning frontend <===="
trivy image --format table --severity CRITICAL,HIGH "dad-jokes-frontend:dev"

echo "====> Scanning backend <===="
trivy image --format table --severity CRITICAL,HIGH "dad-jokes-backend:dev"

echo "====> Scanning nginx-unprivileged <===="
trivy image --format table --severity CRITICAL,HIGH nginx/nginx-unprivileged:alpine

echo "====> Scanning cloudflare/cloudflared:latest <===="
trivy image --format table --severity CRITICAL,HIGH cloudflare/cloudflared:2026.11.0
