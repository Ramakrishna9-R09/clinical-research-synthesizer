from __future__ import annotations

import requests

from app.config import get_settings


class LLMClient:
    def complete(self, prompt: str, system: str | None = None) -> str:
        settings = get_settings()
        try:
            response = requests.post(
                f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                json={"model": settings.ollama_model, "prompt": _join(system, prompt), "stream": False},
                timeout=20,
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception:
            return self._fallback(prompt)

    def _fallback(self, prompt: str) -> str:
        return (
            "Local LLM is not reachable, so this deterministic fallback produced a conservative clinical synthesis. "
            "Use Ollama for richer language generation. The recommendation is limited to cited evidence and should be reviewed by a clinician."
        )


def _join(system: str | None, prompt: str) -> str:
    return f"{system}\n\n{prompt}" if system else prompt
