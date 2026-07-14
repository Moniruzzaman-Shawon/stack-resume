import unittest
from unittest.mock import patch, MagicMock
import json
from resume_review.services.ai_service import analyze_resume, AIAnalysisError


MOCK_AI_RESPONSE = json.dumps({
    "strengths": ["Good formatting", "Clear contact info"],
    "weaknesses": ["Missing summary", "Too short"],
    "missing_skills": ["Python", "SQL"],
    "suggestions": ["Add a professional summary", "Include more metrics"],
    "overall_score": 72,
})


class TestAIAnalysis(unittest.TestCase):

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_returns_dict(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MOCK_AI_RESPONSE
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Test resume")
        self.assertIsInstance(result, dict)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_has_required_fields(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MOCK_AI_RESPONSE
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        for field in ["strengths", "weaknesses", "missing_skills", "suggestions", "overall_score"]:
            self.assertIn(field, result)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_score_clamped_to_100(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": [], "weaknesses": [], "missing_skills": [],
            "suggestions": [], "overall_score": 150,
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertLessEqual(result["overall_score"], 100)
        self.assertGreaterEqual(result["overall_score"], 0)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_score_clamped_to_0(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": [], "weaknesses": [], "missing_skills": [],
            "suggestions": [], "overall_score": -10,
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertGreaterEqual(result["overall_score"], 0)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_score_is_integer(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": [], "weaknesses": [], "missing_skills": [],
            "suggestions": [], "overall_score": 82.5,
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result["overall_score"], int)
        self.assertEqual(result["overall_score"], 82)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_strips_markdown_fences(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "```json\n" + MOCK_AI_RESPONSE + "\n```"
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result, dict)
        self.assertIn("overall_score", result)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_strips_fences_without_newline(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "```" + MOCK_AI_RESPONSE + "```"
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result, dict)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_strips_plain_markdown_fence(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "```\n" + MOCK_AI_RESPONSE + "\n```"
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result, dict)

    def test_missing_api_key_raises(self):
        with patch("resume_review.services.ai_service.os.getenv", return_value=None):
            with self.assertRaises(AIAnalysisError):
                analyze_resume("Test")

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_invalid_json_raises(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "not valid json at all"
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        with self.assertRaises(AIAnalysisError):
            analyze_resume("Sample")

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_missing_fields_raises(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": ["Good"],
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        with self.assertRaises(AIAnalysisError):
            analyze_resume("Sample")

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_text_truncation(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = MOCK_AI_RESPONSE
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        long_text = "A" * 10000
        result = analyze_resume(long_text)
        self.assertIsInstance(result, dict)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_non_list_fields_converted(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": "Single string instead of list",
            "weaknesses": [],
            "missing_skills": [],
            "suggestions": [],
            "overall_score": 70,
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result["strengths"], list)

    @patch("resume_review.services.ai_service.os.getenv", return_value="test-key")
    @patch("resume_review.services.ai_service.StrOutputParser")
    @patch("resume_review.services.ai_service.ChatPromptTemplate")
    @patch("resume_review.services.ai_service.ChatGoogleGenerativeAI")
    def test_empty_string_fields_converted(self, mock_chat, mock_prompt, mock_parser, mock_getenv):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = json.dumps({
            "strengths": "",
            "weaknesses": [],
            "missing_skills": [],
            "suggestions": [],
            "overall_score": 50,
        })
        mock_prompt.from_messages.return_value.__or__ = MagicMock(return_value=MagicMock(__or__=MagicMock(return_value=mock_instance)))

        result = analyze_resume("Sample")
        self.assertIsInstance(result["strengths"], list)


if __name__ == "__main__":
    unittest.main()
