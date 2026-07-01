import os

# ===============================
# Project Directories
# ===============================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")

PAPERS_DIR = os.path.join(DATA_DIR, "papers")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")

TEMP_DIR = os.path.join(BASE_DIR, "temp")

MODELS_DIR = os.path.join(BASE_DIR, "models")


# Automatically create folders
for folder in [
    DATA_DIR,
    PAPERS_DIR,
    REPORTS_DIR,
    TEMP_DIR,
    MODELS_DIR
]:
    os.makedirs(folder, exist_ok=True)


# ===============================
# AI Models
# ===============================

SUMMARIZATION_MODEL = "facebook/bart-large-cnn"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

KEYWORD_MODEL = "all-MiniLM-L6-v2"


# ===============================
# PDF Settings
# ===============================

MAX_PREVIEW_CHARACTERS = 5000

SUPPORTED_FILE_TYPES = [
    "pdf"
]


# ===============================
# Report Settings
# ===============================

REPORT_FILENAME = "Research_Report.docx"


# ===============================
# Streamlit
# ===============================

APP_TITLE = "AI Scientist"

PAGE_ICON = "📚"

LAYOUT = "wide"