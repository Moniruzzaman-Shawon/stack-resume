import unittest
from io import BytesIO
from pypdf import PdfWriter
from resume_review.services.pdf_service import extract_text_from_pdf, PdfExtractionError


def create_test_pdf() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer.read()


class TestPDFExtraction(unittest.TestCase):

    def test_extract_returns_string(self):
        pdf_bytes = create_test_pdf()
        result = extract_text_from_pdf(pdf_bytes)
        self.assertIsInstance(result, str)

    def test_extract_from_empty_page_returns_empty(self):
        pdf_bytes = create_test_pdf()
        result = extract_text_from_pdf(pdf_bytes)
        self.assertEqual(result.strip(), "")

    def test_extract_from_multi_page_pdf(self):
        writer = PdfWriter()
        writer.add_blank_page(width=612, height=792)
        writer.add_blank_page(width=612, height=792)
        buf = BytesIO()
        writer.write(buf)
        buf.seek(0)

        result = extract_text_from_pdf(buf.read())
        self.assertIsInstance(result, str)

    def test_invalid_pdf_raises_extraction_error(self):
        with self.assertRaises(PdfExtractionError):
            extract_text_from_pdf(b"not a pdf at all")

    def test_empty_bytes_raises_extraction_error(self):
        with self.assertRaises(PdfExtractionError):
            extract_text_from_pdf(b"")

    def test_truncated_pdf_raises_extraction_error(self):
        with self.assertRaises(PdfExtractionError):
            extract_text_from_pdf(b"%PDF-1.4 truncated")


if __name__ == "__main__":
    unittest.main()
