import pytest

from extraction.file_content_extraction import extract_text
from backend.process.match_score_resume import score_match
from schema import MatchResult
from pytest import mark 

@pytest.mark.slow
def test_score_match_returns_valid_result():
    resume = extract_text("tests/fixtures/resume.pdf")
    job_description = extract_text("tests/fixtures/job_description.txt")

    result = score_match(resume, job_description)

    assert isinstance(result, MatchResult)
    assert 0 <= result.match_score <= 100
    assert len(result.matched_skills) > 0
    assert len(result.missing_skills) > 0
    assert result.experience_gap
    assert result.rationale
