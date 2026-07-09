from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Iterator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("clinical_research_synthesizer")


@contextmanager
def timed_span(name: str, **fields) -> Iterator[dict]:
    started = time.perf_counter()
    span = {"name": name, **fields}
    logger.info("span.start", extra={"span": span})
    try:
        yield span
    except Exception:
        logger.exception("span.error", extra={"span": span})
        raise
    finally:
        span["duration_ms"] = round((time.perf_counter() - started) * 1000)
        logger.info("span.end", extra={"span": span})
