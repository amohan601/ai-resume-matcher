

from schema import MatchResult
from config import get_job_match_model
from langchain.agents.structured_output import ProviderStrategy 
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from prompts import RESUME_JOB_MATCH_PROMPT


def build_scoring_agent():
    """Build once, reusable across calls — this is the create_agent() part."""
    return create_agent(
        model = get_job_match_model(),
        system_prompt=RESUME_JOB_MATCH_PROMPT,
        response_format = ProviderStrategy(MatchResult)        
    )


def match_score_resume(resume_text: str, job_description: str, agent = None) -> MatchResult: 
    """This is where .invoke() happens — the actual call."""
    print("Scoring match...")
    agent = agent or build_scoring_agent()

    result = agent.invoke({
        "messages": [HumanMessage(content=f"Resume in text: {resume_text}\n\n Job description: {job_description}")
        ]
    })
    print("Raw agent result:", result )
    return result["structured_response"]