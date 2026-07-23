# Contributing

## Development setup

The wrapped `memsearch` library is not on PyPI. On forge, develop from the shared venv
that already has it installed:

```bash
/opt/venvs/memsearch/bin/pip install -e ".[dev]"
```

Elsewhere, the test suite stubs `memsearch` automatically (see `tests/conftest.py`), so
a plain `pip install -e ".[dev]"` is enough to run the tests.

## Running tests

```bash
pytest --cov=memsearch_mcp --cov-report=term-missing   # must stay >= 80%
```

## Linting

```bash
ruff check .
ruff format --check .
```

## Code style

- Python 3.11+, type annotations throughout
- `structlog` JSON logging — never log tool arguments beyond query strings / counts
- `index_memory` only accepts paths under `_ALLOWED_INDEX_ROOTS`; do not widen without a
  security review (resolved from a 2026-05-28 audit finding)

## Releasing

1. Update `CHANGELOG.md` (move `[Unreleased]` to a versioned section).
2. Bump `version` in `pyproject.toml`.
3. Tag `vX.Y.Z` after the PR merges.
