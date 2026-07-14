import logging
from io import BytesIO
from pypdf import PdfReader
from pypdf.errors import PdfReadError

logger = logging.getLogger("resume_review")


class PdfExtractionError(Exception):
    pass


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts)

    except PdfReadError as e:
        logger.warning("PDF read error: %s", str(e))
        raise PdfExtractionError(f"Failed to read PDF: {e}") from e
    except Exception as e:
        logger.exception("Unexpected error extracting PDF text")
        raise PdfExtractionError(f"Failed to extract text from PDF") from e
