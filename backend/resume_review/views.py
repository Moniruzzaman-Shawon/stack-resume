import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.pdf_service import extract_text_from_pdf, PdfExtractionError
from .services.ai_service import analyze_resume, AIAnalysisError

logger = logging.getLogger("resume_review")

MAX_FILE_SIZE = 5 * 1024 * 1024
PDF_MAGIC_BYTES = b"%PDF"


@api_view(["POST"])
def review_resume(request):
    uploaded_file = request.FILES.get("resume")

    if not uploaded_file:
        return Response(
            {"error": "No file uploaded. Please upload a PDF resume."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not uploaded_file.name.lower().endswith(".pdf"):
        return Response(
            {"error": "Invalid file type. Please upload a PDF file."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if uploaded_file.size > MAX_FILE_SIZE:
        return Response(
            {"error": "File too large. Maximum size is 5MB."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        pdf_bytes = uploaded_file.read()

        if not pdf_bytes[:4] == PDF_MAGIC_BYTES:
            return Response(
                {"error": "Invalid PDF file. Please upload a valid PDF."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        extracted_text = extract_text_from_pdf(pdf_bytes)

        if not extracted_text.strip():
            return Response(
                {"error": "Could not extract text from the PDF. The file may be scanned or empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = analyze_resume(extracted_text)
        return Response(result, status=status.HTTP_200_OK)

    except ValueError as e:
        logger.warning("Validation error: %s", str(e))
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except AIAnalysisError as e:
        logger.error("AI analysis failed: %s", str(e))
        return Response(
            {"error": "Failed to analyze resume. Please try again later."},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    except PdfExtractionError as e:
        logger.warning("PDF extraction failed: %s", str(e))
        return Response(
            {"error": "Failed to read the PDF file. It may be corrupted or password-protected."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.exception("Unexpected error processing resume")
        return Response(
            {"error": "An unexpected error occurred. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
