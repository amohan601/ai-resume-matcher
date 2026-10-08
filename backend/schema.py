
from pydantic import BaseModel,Field
from datetime import date   

class MatchResult(BaseModel):
    match_score: float = Field(description="Score indicating how well the resume matches the job description ge >= 0 and le<= 100 where 100 is perfect match and 0 is no match")     
    matched_skills: list[str] = Field(description="Match skills list")     
    missing_skills: list[str] = Field(description="Missing skills description")     
    experience_gap: str = Field(description="Experience gap description")     
    rationale: str = Field(description="Explanation for the match score")

class RewrittenResume(BaseModel):
    tailored_resume: str = Field(description="The full rewritten resume text, reordered and rephrased to fit the job description, using only information already present in the original resume — no invented experience, skills, or numbers")
    changes_summary: str = Field(description="A short summary of what was changed and why, e.g. which sections were reordered or emphasized")
    
class Application(BaseModel):
    user_id: str
    company: str
    role: str
    source: str | None = None
    job_description: str | None = None
    applied_date: date = date.today()
    status: str | None = None
