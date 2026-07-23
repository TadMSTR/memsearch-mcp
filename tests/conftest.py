"""Test bootstrap for memsearch-mcp.

The wrapped ``memsearch`` library is not published to PyPI, so it cannot be
installed in GitHub CI. The unit tests mock every call into it, so we only need
``import memsearch`` / ``from memsearch.config import resolve_config`` to resolve
and the module-level ``MemSearch(...)`` init in ``server.py`` to construct without
crashing.

When the real library IS importable (the forge ``/opt/venvs/memsearch`` venv), it
is used unchanged. Otherwise we register a minimal stub in ``sys.modules`` before
``memsearch_mcp.server`` is first imported.
"""

from __future__ import annotations

import sys
import types
from types import SimpleNamespace


def _install_memsearch_stub() -> None:
    memsearch = types.ModuleType("memsearch")

    class _StubMemSearch:
        def __init__(self, *args, **kwargs) -> None:
            self._kwargs = kwargs

        async def search(self, query, top_k=10):  # pragma: no cover - mocked in tests
            return []

        async def index(self):  # pragma: no cover - mocked in tests
            return 0

        async def index_file(self, path):  # pragma: no cover - mocked in tests
            return 0

        def close(self) -> None:  # pragma: no cover - mocked in tests
            return None

    memsearch.MemSearch = _StubMemSearch

    config = types.ModuleType("memsearch.config")

    def resolve_config():
        return SimpleNamespace(
            embedding=SimpleNamespace(
                provider="stub",
                model="",
                batch_size=8,
                base_url="",
                api_key="",
            ),
            milvus=SimpleNamespace(uri="stub://milvus", token="", collection="stub"),
            chunking=SimpleNamespace(max_chunk_size=512, overlap_lines=2),
            reranker=SimpleNamespace(model=""),
        )

    config.resolve_config = resolve_config
    memsearch.config = config

    sys.modules.setdefault("memsearch", memsearch)
    sys.modules.setdefault("memsearch.config", config)


try:
    import memsearch
    import memsearch.config  # noqa: F401
except ImportError:
    _install_memsearch_stub()
