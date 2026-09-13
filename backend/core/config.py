import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

#api metadata
API_TITLE = "ATS RESUME ANALYZER API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "analyze resumes and job descriptions to find the best matches(using nlp + ml)"

ALLOWED_ORIGINS = [
    "http://localhost:5173", #Vite dev server (React)
    "http://localhost:3000", #Create React app fallback
    "http://127.0.0.1:5173",
]

#file
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

#supported MIME types and their short names
SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

SUPPORTED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

SPACY_MODEL_PRIMARY = "en_core_web_md" #better accuracy
SPACY_MODEL_SECONDARY = "en_core_web_sm" #faster processing
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

#score component weights - this is business logic treated as config
SCORE_WEIGHTS = {
    "formatting": 20, "keywords": 25, "content": 25,
    "skill_validation": 15, "ats_compatibility": 15
}

#GROQ API key for semantic search
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
