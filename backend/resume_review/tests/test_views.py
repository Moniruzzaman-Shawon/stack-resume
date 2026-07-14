import unittest
from io import BytesIO
from unittest.mock import patch
from rest_framework.test import APIRequestFactory
from resume_review.views import review_resume
from resume_review.services.ai_service import AIAnalysisError
from resume_review.services.pdf_service import PdfExtractionError


factory = APIRequestFactory()


def make_pdf_bytes():
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = BytesIO()
    writer.write(buf)
    buf.seek(0)
    return buf.read()


def make_upload_request(pdf_bytes, filename="resume.pdf", content_type="application/pdf"):
    uploaded_file = BytesIO(pdf_bytes)
    uploaded_file.name = filename
    uploaded_file.content_type = content_type
    uploaded_file.size = len(pdf_bytes)
    return factory.post("/api/review/", {"resume": uploaded_file}, format="multipart")


class TestReviewEndpoint(unittest.TestCase):

    def test_no_file_returns_400(self):
        request = factory.post("/api/review/")
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_non_pdf_extension_returns_400(self):
        request = make_upload_request(b"fake", filename="resume.txt", content_type="text/plain")
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)

    def test_oversized_file_returns_400(self):
        content = b"x" * (5 * 1024 * 1024 + 1)
        uploaded_file = BytesIO(content)
        uploaded_file.name = "resume.pdf"
        uploaded_file.content_type = "application/pdf"
        uploaded_file.size = len(content)
        request = factory.post("/api/review/", {"resume": uploaded_file}, format="multipart")
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)

    def test_over_5mb_rejected(self):
        content = b"%PDF-1.4" + b"\x00" * (5 * 1024 * 1024)
        uploaded_file = BytesIO(content)
        uploaded_file.name = "resume.pdf"
        uploaded_file.content_type = "application/pdf"
        uploaded_file.size = len(content)
        request = factory.post("/api/review/", {"resume": uploaded_file}, format="multipart")
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_pdf_magic_bytes_returns_400(self):
        request = make_upload_request(b"not a pdf at all")
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)

    @patch("resume_review.views.analyze_resume")
    @patch("resume_review.views.extract_text_from_pdf")
    def test_valid_pdf_returns_200(self, mock_extract, mock_analyze):
        mock_extract.return_value = "John Doe\nSoftware Engineer"
        mock_analyze.return_value = {
            "strengths": ["Good"],
            "weaknesses": ["Short"],
            "missing_skills": ["Python"],
            "suggestions": ["Add more"],
            "overall_score": 70,
        }

        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn("overall_score", response.data)

    @patch("resume_review.views.extract_text_from_pdf")
    def test_empty_pdf_text_returns_400(self, mock_extract):
        mock_extract.return_value = ""
        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)

    @patch("resume_review.views.analyze_resume")
    @patch("resume_review.views.extract_text_from_pdf")
    def test_response_contains_all_fields(self, mock_extract, mock_analyze):
        mock_extract.return_value = "Test resume content"
        mock_analyze.return_value = {
            "strengths": ["S1"],
            "weaknesses": ["W1"],
            "missing_skills": ["M1"],
            "suggestions": ["G1"],
            "overall_score": 80,
        }

        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 200)
        for key in ["strengths", "weaknesses", "missing_skills", "suggestions", "overall_score"]:
            self.assertIn(key, response.data)

    @patch("resume_review.views.extract_text_from_pdf")
    def test_pdf_extraction_error_returns_400(self, mock_extract):
        mock_extract.side_effect = PdfExtractionError("Corrupted PDF")
        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    @patch("resume_review.views.analyze_resume")
    @patch("resume_review.views.extract_text_from_pdf")
    def test_ai_analysis_error_returns_502(self, mock_extract, mock_analyze):
        mock_extract.return_value = "Valid text"
        mock_analyze.side_effect = AIAnalysisError("OpenAI API error")
        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 502)
        self.assertIn("error", response.data)

    @patch("resume_review.views.extract_text_from_pdf")
    def test_generic_exception_returns_500(self, mock_extract):
        mock_extract.side_effect = RuntimeError("Something unexpected")
        request = make_upload_request(make_pdf_bytes())
        response = review_resume(request)
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.data)
        self.assertNotIn("Something unexpected", response.data["error"])


if __name__ == "__main__":
    unittest.main()
