# Security Policy

## Reporting a Vulnerability

Please do not open a public issue with exploit details.

Prefer [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) for this repository when it is enabled. If that is unavailable, contact the maintainers directly and include:

- Affected files and (approximate) line numbers
- Clear reproduction steps
- Impact assessment
- Any suggested mitigation

We will acknowledge reports as soon as practical and coordinate a fix before any public disclosure.

## Automated scanning

CI (see [`.github/workflows/ci.yml`](.github/workflows/ci.yml)) runs two security gates:

### Snyk Code

- Runs when the `SNYK_TOKEN` repository secret is configured
- Skips cleanly when the token is absent (forks and local clones without secrets)
- Uploads SARIF results to GitHub Code Scanning when available
- Fails the workflow on high-severity findings

Policy exclusions live in [`.snyk`](.snyk) (generated assets and report trees). IDE / DeepCode ignores live in [`.dcignore`](.dcignore).

### detect-secrets

- Local pre-commit hook via [`.pre-commit-config.yaml`](.pre-commit-config.yaml)
- CI pull-request gate that fails on findings not already in [`.secrets.baseline`](.secrets.baseline)

Install and enable the hook:

```bash
pip install pre-commit
pre-commit install
```

Refresh the baseline after intentional allow-list changes:

```bash
detect-secrets scan --all-files --exclude-files '(^|[\\/])\.venv([\\/]|$)' > .secrets.baseline
```

## Secrets and credentials

- Never commit API keys, tokens, or `.env` files. Use [`.env.example`](.env.example) as a template for local configuration.
- Prefer environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `FRED_API_KEY`, etc.) over hard-coding credentials in scripts or notebooks.
- Rotate any credential that may have been exposed in a commit, CI log, or shared artifact.

## Canary token placement

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
