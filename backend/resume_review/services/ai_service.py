import json
import logging
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger("resume_review")

SYSTEM_PROMPT = """You are an expert resume reviewer and career coach. Analyze the following resume text and provide a detailed, structured review.

Return your analysis as a JSON object with exactly these fields:
{
  "strengths": ["list of strengths found in the resume"],
  "weaknesses": ["list of weaknesses or areas needing improvement"],
  "missing_skills": ["skills or keywords commonly expected but missing"],
  "suggestions": ["specific actionable suggestions to improve the resume"],
  "overall_score": <integer between 0 and 100>
}

Guidelines for scoring:
- 90-100: Exceptional resume, ready for top companies
- 70-89: Good resume with minor improvements needed
- 50-69: Average resume, needs significant improvements
- Below 50: Needs major restructuring and content additions

Be specific, constructive, and actionable in your feedback. Focus on content, structure, keywords, and impact.

IMPORTANT: Return ONLY the JSON object, no additional text or markdown formatting."""

MAX_TEXT_LENGTH = 8000

_llm_instance = None


class AIAnalysisError(Exception):
    pass


def _get_llm():
    global _llm_instance
    if _llm_instance is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise AIAnalysisError("GOOGLE_API_KEY environment variable is not set")
        _llm_instance = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key,
        )
    return _llm_instance


def _parse_json_response(response: str) -> dict:
    response = response.strip()

    if "```" in response:
        import re
        response = re.sub(r"^```(?:json)?\s*\n?", "", response)
        response = re.sub(r"\n?```\s*$", "", response)
        response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise AIAnalysisError(f"Failed to parse AI response as JSON: {e}") from e


def _validate_result(result: dict) -> dict:
    required_fields = ["strengths", "weaknesses", "missing_skills", "suggestions", "overall_score"]
    for field in required_fields:
        if field not in result:
            raise AIAnalysisError(f"AI response missing required field: {field}")

    for field in ["strengths", "weaknesses", "missing_skills", "suggestions"]:
        if not isinstance(result[field], list):
            result[field] = [str(result[field])] if result[field] else []

    result["overall_score"] = max(0, min(100, int(result["overall_score"])))

    return result


def analyze_resume(text: str) -> dict:
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    try:
        llm = _get_llm()

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Please review this resume:\n\n{text}"),
        ])

        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"text": text})

        result = _parse_json_response(response)
        return _validate_result(result)

    except AIAnalysisError:
        raise
    except Exception as e:
        logger.exception("AI analysis failed")
        raise AIAnalysisError(f"AI service error: {type(e).__name__}") from e
