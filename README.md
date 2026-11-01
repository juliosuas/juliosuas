# Julio César Suástegui

Full-stack engineer in Mexico City. TypeScript, React, Python, Cloudflare, Supabase.
I ship with tests, CI and review, in my own products and in open source.

**49 merged PRs across 16 external open-source repos**, including 9 in `microsoft/PyRIT` and 16 in `soxoj/maigret`.

## Selected work

### PyRIT datasets catalog GUI ([microsoft/PyRIT #3071](https://github.com/microsoft/PyRIT/pull/3071))
- **Problem:** PyRIT users had no visual way to browse datasets.
- **Action:** Built a full-stack catalog (frontend and backend, about 2,300 lines across 25 files) and iterated through maintainer review.
- **Result:** Merged by Microsoft.

### Race condition in pagination and refresh ([microsoft/PyRIT #2745](https://github.com/microsoft/PyRIT/issues/2745))
- **Problem:** The table's pagination and refresh raced and showed stale data.
- **Action:** Fixed the ordering and added tests against a real backend with seeded data. Removed an out-of-scope commit before pushing.
- **Result:** All tests green, fix merged.

### Aivumo (own product)
- React + TypeScript + Vite + shadcn/ui frontend, Supabase backend, Cloudflare deploy.
- CI: lint, typecheck, build and Pages artifact verification on every PR.

## Other open source
mitmproxy, kellyjonbrazil/jc, aquasecurity/trivy, getsentry/sentry-python, getsentry/responses, zeek/package-manager, CycloneDX, OWASP, locust, palantir/blueprint.

## How I work
Small scoped PRs, issue claimed before code, maintainer guidelines first, tests on every change.
