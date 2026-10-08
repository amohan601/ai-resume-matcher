from langchain_core.tools import tool 
from schema import RewrittenResume
from langchain.agents import create_agent
from prompts import REWRITE_RESUME_PROMPT
from config import get_job_match_model
from langchain.messages import HumanMessage
from langchain.agents.structured_output import ProviderStrategy 
"""
Actual resume generation agent.
"""
def build_generate_resume_agent():
    return create_agent(
        model = get_job_match_model(),
        system_prompt = REWRITE_RESUME_PROMPT,
        response_format = ProviderStrategy(RewrittenResume)
    )


@tool
def generate_resume(original_resume: str, job_description: str) -> RewrittenResume:
    """Generate the resume tailored to the job description, using only information already present in the original resume."""
    print("Generating tailored resume...",original_resume[:30], job_description[:30])
    agent = build_generate_resume_agent()
    result = agent.invoke({
        "messages":[
            HumanMessage(content=f"Original resume: {original_resume}\n\nJob description: {job_description}")
        ]
    })
    print("Generate resume agent result:", result)
    
    return result["structured_response"]


