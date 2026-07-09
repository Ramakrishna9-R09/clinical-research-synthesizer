import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass
class Settings:
    app_name: str = "Clinical Research Synthesizer"
    app_env: str = "local"
    data_dir: Path = Path("./data")
    report_dir: Path = Path("./reports")
    index_dir: Path = Path("./storage/chroma")
    cache_dir: Path = Path("./storage/cache")
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    tavily_api_key: str | None = None
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "clinical-research-synthesizer"


@lru_cache
def get_settings() -> Settings:
    _load_dotenv()
    default_data_dir = "/tmp/clinical-data" if os.getenv("VERCEL") else "./data"
    default_report_dir = "/tmp/clinical-reports" if os.getenv("VERCEL") else "./reports"
    default_index_dir = "/tmp/clinical-index" if os.getenv("VERCEL") else "./storage/chroma"
    default_cache_dir = "/tmp/clinical-cache" if os.getenv("VERCEL") else "./storage/cache"
    settings = Settings(
        app_name=os.getenv("APP_NAME", "Clinical Research Synthesizer"),
        app_env=os.getenv("APP_ENV", "local"),
        data_dir=Path(os.getenv("DATA_DIR", default_data_dir)),
        report_dir=Path(os.getenv("REPORT_DIR", default_report_dir)),
        index_dir=Path(os.getenv("INDEX_DIR", default_index_dir)),
        cache_dir=Path(os.getenv("CACHE_DIR", default_cache_dir)),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        tavily_api_key=os.getenv("TAVILY_API_KEY") or None,
        langsmith_tracing=os.getenv("LANGSMITH_TRACING", "false").lower() == "true",
        langsmith_api_key=os.getenv("LANGSMITH_API_KEY") or None,
        langsmith_project=os.getenv("LANGSMITH_PROJECT", "clinical-research-synthesizer"),
    )
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.report_dir.mkdir(parents=True, exist_ok=True)
    settings.index_dir.mkdir(parents=True, exist_ok=True)
    settings.cache_dir.mkdir(parents=True, exist_ok=True)
    return settings


def _load_dotenv() -> None:
    path = Path(".env")
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
