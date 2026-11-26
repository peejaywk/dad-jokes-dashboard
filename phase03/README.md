# Phase 3: Image pipeline

  Phase 3 moves the app out of the phase folders into `apps/`, and GitHub Actions now tests, scans, versions and
  publishes each image.

## Repo layout

  ```
  apps/
    api/        FastAPI backend (uv, ruff, pytest)
    web/        nginx frontend (static page, proxies /api)
  .github/workflows/
    api-ci.yaml         checks on every API pull request
    web-ci.yaml         checks on every web pull request
    release-please.yaml opens release PRs from main
    api-publish.yaml    pushes the API image to GHCR on an api-v* tag
    web-publish.yaml    pushes the web image to GHCR on a web-v* tag
  phase01/, phase02/    earlier phases, kept for reference
  ```

  Each app has its own version, its own `CHANGELOG.md` and its own image.

## How a change becomes an image

  ```
  pull request ──▶ CI: lint, tests, build, Trivy scan
       │ merge to main (manual process)
       ▼
  release-please ──▶ opens a release PR (version bump + changelog)
       │ merge the release PR (manual process)
       ▼
  tag api-vX.Y.Z / web-vX.Y.Z ──▶ publish: build and push to GHCR
  ```

  1. **Pull request.** CI runs only for the app that changed. The API job lints with ruff, runs pytest (it fails below
  80% coverage and posts the coverage on the PR), builds the image and scans it with Trivy. The web job builds the image
  and scans it. Trivy fails the build on fixable critical or high vulnerabilities.
  2. **Merge to main.** Release Please reads the conventional commit messages (`feat:`, `fix:`) and opens a separate
  release PR for each app that changed.
  3. **Merge the release PR.** This creates a tag such as `api-v0.2.0`, which triggers that app's publish workflow.
  4. **Publish.** The image goes to GHCR tagged with its version and `latest`:
     - `ghcr.io/peejaywk/dad-jokes-api`
     - `ghcr.io/peejaywk/dad-jokes-web`

## Notes

- Commit messages must be conventional commits. A pre-commit hook (commitizen) checks them, because Release Please
  works out the next version from them.
- Release Please uses a personal access token (`DAD_JOKE_TOKEN`), because tags created with the default `GITHUB_TOKEN`
  don't trigger other workflows.
- Third-party actions are pinned to commit SHAs.

## Still to do

- Renovate raises a PR when a new image version is published.
