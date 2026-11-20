#!/bin/bash
# Build the container images and scan both containers for vulnerabilities with Trivy.
# Usage: ./build-scan.sh

# This will stop the script if the build fails.
set -euo pipefail

# Run from this script's folder so the Docker build finds the Dockerfile.
cd "$(dirname "$0")"

#echo "====> Build frontend and backend containers <===="
docker compose build

echo "====> Scanning frontend <===="
trivy image --format table --severity CRITICAL,HIGH "dad-jokes-frontend:dev"

echo "====> Scanning backend <===="
trivy image --format table --severity CRITICAL,HIGH "dad-jokes-backend:dev"

echo "====> Scanning nginx-unprivileged <===="
trivy image --format table --severity CRITICAL,HIGH nginx/nginx-unprivileged:alpine

echo "====> Scanning cloudflare/cloudflared:2026.11.0 <===="
trivy image --format table --severity CRITICAL,HIGH cloudflare/cloudflared:2026.11.0
