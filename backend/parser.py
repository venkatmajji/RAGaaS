import io
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document
import csv

SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".docx", ".csv"]

def extract_text(filename: str, file_bytes: bytes) -> Optional[str]:
    """
    Extracts text content from uploaded file based on extension.
    Supports: .txt, .pdf, .docx, .csv
    """
    try:
        if filename.endswith(".txt"):
            return file_bytes.decode("utf-8")

        elif filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n".join([
                page.extract_text()
                for page in reader.pages
                if page.extract_text()
            ])

        elif filename.endswith(".docx"):
            doc = Document(io.BytesIO(file_bytes))
            return "\n".join([para.text for para in doc.paragraphs])

        elif filename.endswith(".csv"):
            decoded = file_bytes.decode("utf-8")
            reader = csv.reader(io.StringIO(decoded))
            rows = [" | ".join(row) for row in reader]
            return "\n".join(rows)

        else:
            print(f"[PARSER] Unsupported file type: {filename}")
            return None

    except Exception as e:
        print(f"[PARSER ERROR] Failed to extract from {filename}: {e}")
        return None
