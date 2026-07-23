# Architecture

`memsearch-mcp` is a thin FastMCP server that exposes the
[`memsearch`](https://github.com/TadMSTR/memsearch) hybrid (vector + BM25 + reranker)
search library to forge agents over streamable-HTTP MCP.

## Components

```
src/memsearch_mcp/
  __init__.py
  server.py     # FastMCP app, 2 tools, MemSearch init, bearer-auth middleware, path allowlist
  models.py     # MemoryResult pydantic model + infer_tier()
tests/
  conftest.py   # stubs `memsearch` when the real lib is unavailable (CI)
  test_server.py
```

- **Transport:** streamable-HTTP, bound to `127.0.0.1:8493` (loopback only).
- **Framework:** FastMCP (`fastmcp>=3.2.4,<4`).
- **Backend:** `memsearch` library over Milvus; config resolved via
  `memsearch.config.resolve_config()` (not this server's env).
- **Logging:** `structlog`, JSON output.

## Tools

| Tool | Description |
|------|-------------|
| `search_memory(query, limit=10)` | Hybrid search; returns `MemoryResult` dicts (path, score, snippet, heading, tier, line span). Errors are returned as `[{"error": ...}]`, never raised. |
| `index_memory(path=None)` | Re-index a file or directory. Path must resolve within `_ALLOWED_INDEX_ROOTS`. |

## Security model

- **Loopback-only** — binds to `127.0.0.1`.
- **Optional bearer auth** — `_BearerAuthMiddleware` activates when `MEMSEARCH_API_TOKEN`
  is set; constant-time comparison via `hmac.compare_digest`; 401 otherwise.
- **`index_memory` allowlist** — `_ALLOWED_INDEX_ROOTS` (`~/.claude/memory`,
  `~/.claude/projects`, `/opt/agents/memory`), enforced with `Path.is_relative_to()` after
  `resolve()`. Denylisted for security/research/writer agents at the scoped-mcp layer.
- **Tier inference** — `infer_tier()` uses `Path.is_relative_to()` (not substring matching)
  so crafted paths can't spoof a trusted tier.

## Deployment

Runs as a PM2 process (`ecosystem.config.js`) via `-m memsearch_mcp.server` out of the
`/opt/venvs/memsearch` virtualenv, which also provides the `memsearch` library.
