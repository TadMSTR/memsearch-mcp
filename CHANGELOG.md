# Changelog

## [Unreleased]

## [0.2.0] — 2026-07-23

### Security

- **Bearer token authentication** — optional `_BearerAuthMiddleware` ASGI middleware
  activated when `MEMSEARCH_API_TOKEN` is set. Uses `hmac.compare_digest()` for
  constant-time token comparison. Returns 401 JSON error for invalid/missing tokens.
  Disabled by default (logs warning at startup when no token configured).

### Changed

- **Repo brought to the forge Python-MCP standard.** Migrated to a `src/memsearch_mcp/`
  layout (package import path and PM2 entry point `-m memsearch_mcp.server` unchanged;
  needs a `pip install -e .` refresh in the venv on cutover).
- Bumped `fastmcp` pin `>=2.0` → `>=3.2.4,<4` (matches the installed 3.x and sibling repos).

### Added

- MIT `LICENSE`.
- CI workflow (`.github/workflows/ci.yml`) — 3.11/3.12/3.13 matrix, SHA-pinned actions;
  `ruff check` + `ruff format --check` + `pytest --cov` (fail-under 80) + `pip-audit --strict`.
- `ruff` + coverage config; `.gitleaks.toml`; `CONTRIBUTING.md`; `ARCHITECTURE.md`.
- `tests/conftest.py` stub so the suite runs without the (non-PyPI) `memsearch` library.
- Tests for the `index_memory` file/directory branches and the `main()` entry point
  (coverage 77% → ≥80%).

### Fixed

- Added `.env` and `*.env` to `.gitignore` to prevent accidental token commits.

### Security (audit)

- Audit `memory-mcp-trio-repo-standard-2026-07` (2026-07-23): clean — bearer-auth and
  `index_memory` path allowlist verified intact through the src/ move. 1 Low accepted:
  tool errors return raw exception text to the (loopback, trusted-agent) caller —
  `SECURITY[accepted]` in `server.py`.

## [0.1.0] — 2026-05-29

### Added
- `search_memory(query, limit=10)` — hybrid vector+BM25+reranker semantic search over Milvus-indexed agent memory
- `index_memory(path=None)` — trigger index refresh for allowed memory paths
- Tier labeling: session, working, docs, unknown based on source path
- PM2 deployment on port 8493 using `/opt/venvs/memsearch` Python interpreter
- Registered in all 5 forge agent scoped-mcp manifests

### Security
- `index_memory` restricted to `_ALLOWED_INDEX_ROOTS` whitelist (MEM-01)
- `infer_tier()` uses `Path.is_relative_to()` instead of substring matching (MEM-02)
- `index_memory` denylisted for security, research, and writer agents (MEM-03)
