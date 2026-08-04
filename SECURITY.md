# Security Policy

## Reporting a Vulnerability

If you believe you found a security issue, please do not publish exploit details in a public issue first.

Use GitHub Security Advisories (private reporting) when available for this repository. If that is unavailable, contact the maintainers directly and include:

- Affected files and line numbers
- Reproduction steps
- Impact assessment
- Suggested mitigation

## Secret Scanning Workflow

This repository uses detect-secrets in two places:

- Local pre-commit hook via [.pre-commit-config.yaml](.pre-commit-config.yaml)
- CI pull-request gate via [.github/workflows/ci.yml](.github/workflows/ci.yml)

The baseline file is [.secrets.baseline](.secrets.baseline). CI fails when new findings appear that are not already in the baseline.

## Canary Token Placement Policy

Canary tokens are for leak detection, not authentication.

Rules:

1. Never place canaries in executable runtime configs used by production paths.
2. Place canaries only in clearly labeled non-runtime files, such as `.env.canary.example` or documentation examples.
3. Prefix names clearly, for example `CANARY_DO_NOT_USE`.
4. Scope canaries to low-privilege, monitor-only endpoints.
5. Route token alerts to monitored channels with on-call ownership.
6. Rotate or revoke canaries on any alert and open an incident review.

Operational guidance:

- Treat every canary callback as a potential leak until proven otherwise.
- Correlate callback timestamps with recent commits, CI logs, artifact uploads, and dependency updates.
- If a true leak is confirmed, rotate affected real credentials immediately.

## Developer Setup

Install and enable pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

Run secret scan manually:

```bash
detect-secrets scan --all-files --exclude-files '(^|[\\/])\.venv([\\/]|$)' > .secrets.baseline
```