from pathlib import Path
from pypdf import PdfReader
from docx import Document


def read_document(file_path):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif extension == ".docx":
        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    elif extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    else:
        raise ValueError(
            "Only PDF, DOCX and TXT files are supported."
        )