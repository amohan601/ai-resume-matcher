from schema import MatchResult


def test_match_result():
    result = MatchResult(
        match_score=82,
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Kubernetes"],
        experience_gap="Job wants 5 years, resume shows 3",
        rationale="Good match overall",
    )

    assert result.match_score == 82
    assert result.matched_skills == ["Python", "FastAPI"]
    assert result.missing_skills == ["Kubernetes"]
