#!/bin/bash
# Build the updater image and scan both containers for vulnerabilities with Trivy.
# Usage: ./scan.sh          (uses tag 01)
#        TAG=02 ./scan.sh   (uses another tag)

# This will stop the script if the build fails.
set -euo pipefail

TAG="${TAG:-01}"

# Run from this script's folder so the Docker build finds the Dockerfile.
cd "$(dirname "$0")"

echo "====> Building updater:$TAG <===="
docker build -t "updater:$TAG" .

echo "====> Scanning updater:$TAG <===="
trivy image --format table --severity CRITICAL,HIGH "updater:$TAG"

echo "====> Scanning nginx/nginx-unprivileged:alpine <===="
trivy image --format table --severity CRITICAL,HIGH nginx/nginx-unprivileged:alpine
