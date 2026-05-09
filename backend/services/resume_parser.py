import uuid
import logging
from pathlib import Path

from pypdf import PdfReader
from config import settings
from services.claude_service import parse_resume

logger = logging.getLogger(__name__)


def save_file(content: bytes, filename: str) -> str:
    storage = Path(settings.resume_storage_path)
    storage.mkdir(parents=True, exist_ok=True)
    safe_name = f"{uuid.uuid4()}_{Path(filename).name}"
    path = storage / safe_name
    path.write_bytes(content)
    return str(path.absolute())


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def process_resume(content: bytes, filename: str) -> dict:
    file_path = save_file(content, filename)
    raw_text = extract_pdf_text(file_path)
    logger.info("Extracted %d chars from %s", len(raw_text), filename)
    parsed = parse_resume(raw_text)
    return {"file_path": file_path, "raw_text": raw_text, "parsed": parsed}
