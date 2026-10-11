"""Central settings. Change values here, not inside other files (SRS NFR-19)."""
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
JUDGMENTS_DIR = DATASET_DIR / "judgments"
CASES_JSON = DATASET_DIR / "cases.json"
CACHE_DIR = BASE_DIR / "cache"

MAX_FILE_SIZE_MB = 25          # FR-02: files bigger than this are rejected
TOP_K_RESULTS = 5              # FR-19: show up to 5 similar cases
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# SRS section 8.4: Combined = 0.60*semantic + 0.25*provision + 0.15*keyword
WEIGHT_SEMANTIC = 0.60
WEIGHT_PROVISION = 0.25
WEIGHT_KEYWORD = 0.15

ENABLE_OCR = False             # optional (FR-05)
ENABLE_LLM = False             # optional (Ollama + Qwen2.5 3B)
