# Dad Joke Dashboard – Project Plan

A small multi-container app I'm using to practise the full DevOps workflow: containers, TLS, CI/CD, supply-chain security, Kubernetes and GitOps.

## What it is

Two containers:

- **fetcher**: a small Python API that pulls jokes from a public dad-joke API and caches them
- **web**: nginx serving a static page and proxying `/api` to the fetcher

## Stack

Docker Compose · nginx · Python · Trivy · Cloudflare Tunnel · Caddy · GitHub Actions · GHCR · Renovate · Kubernetes (Rancher Desktop, then k3s) · Gateway API (Traefik) · Flux · SOPS + age

## Phase 1: Containers on Docker

- Build the fetcher and web images and run them together with Docker Compose on my local machine.
- Non-root containers, healthchecks, no secrets in the repo
- Code in GitHub from day one

**Done when:** the dashboard loads on the local IP and the code is stored in GitHub

## Phase 2: Public with TLS

- Route it through my existing Caddy reverse proxy (already handles certs)
- Expose it with a Cloudflare Tunnel, so no inbound ports are opened on the homelab

**Done when:** it's reachable over HTTPS on my domain from outside the house.

## Phase 3: Image pipeline

- Move the fetcher image into its own repo
- GitHub Actions builds on each change, scans with Trivy (fails on fixable critical/high) and publishes semver-tagged images to GHCR
- Renovate raises a PR on the app repo when a new image version is published

**Done when:** a code change ends up as a Renovate PR bumping the image, with no manual steps.

## Phase 4: Kubernetes locally

- Deploy to Rancher Desktop on my Linux dev machine
- Write plain manifests by hand (deployment, service, route) to learn the basics
- Use Gateway API (Traefik) to route traffic to the app

**Done when:** the app is reachable on a local IP through the Gateway.

## Phase 5: GitOps on k3s

- Create the Flux manifests to deploy the app on k3s
- Run cloudflared in the cluster and move the public hostname over from the Docker version
- Encrypt the tunnel token with SOPS + age
- Renovate keeps the image current through PRs; nothing is pushed straight to main

**Done when:** merging a Renovate PR rolls out the new version with no manual `kubectl`.

## Phase 6: Staging cluster

- Build a separate k3s staging cluster on Proxmox, managed by Flux from the same repo
- New image versions go to staging first via Renovate PRs
- Test in staging, then promote the same version to production with a PR
- Staging stays LAN-only

**Done when:** a new image is tested in staging and promoted to production through a PR, with no manual `kubectl`.

## Phase 7 (stretch): Database and high availability

- Add Postgres using the CloudNativePG operator (3 instances, automatic failover)
- Make the API stateless and move joke fetching into a CronJob that writes to the database
- Add up/down voting on jokes, stored in the database, with a "top jokes" view
- Run multiple replicas of the web and API pods
- Database credentials encrypted with SOPS
- Scheduled database backups, with a tested restore
- Run a failover drill and write it up

> My cluster has one node, so this shows pod-level failover. Node-level HA needs more nodes.

**Done when:** I can kill the primary database pod and the app keeps serving and saving votes, and I've restored a backup successfully.

## Open decisions

- Where Renovate runs: GitHub Actions workflow or k3s CronJob
- How staging and production are laid out in the Flux repo (separate folders or shared base + overlays)
- Where database backups go (S3-compatible storage)

## Stretch goals

- SBOM and image signing (cosign)
- Basic monitoring and alerting
