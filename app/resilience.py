from __future__ import annotations

from collections.abc import Callable
import hashlib
import json
import time
from pathlib import Path
from typing import TypeVar

from app.config import get_settings

T = TypeVar("T")


def retry(operation: Callable[[], T], attempts: int = 3, base_delay: float = 0.25) -> T:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(base_delay * (2**attempt))
    assert last_error is not None
    raise last_error


class JsonFileCache:
    def __init__(self, namespace: str):
        self.path = get_settings().cache_dir / f"{namespace}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def get_or_set(self, key_parts: list[str], producer: Callable[[], T]) -> T:
        key = hashlib.sha256("|".join(key_parts).encode("utf-8")).hexdigest()
        if key in self._data:
            return self._data[key]
        value = producer()
        self._data[key] = value
        self._save()
        return value

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
