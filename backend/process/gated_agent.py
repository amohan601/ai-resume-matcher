import uuid

from schema import RewrittenResume
from langchain.agents import create_agent
from prompts import GATEKEEPER_AGENT_PROMPT
from config import get_job_match_model
from langchain.messages import HumanMessage
from langchain.agents.structured_output import ProviderStrategy 
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from process.generate_resume import generate_resume 

"""
Gated agent helping to decide whether to call the generate_resume tool or not. 
This is a separate agent from the generate_resume agent itself, and is used to 
determine whether to call the tool based on the input resume and job description. 
"""
gated_agent = None    
def create_gated_agent():
    print("Building gated agent for resume tailoring check..."  )
    global gated_agent
    gated_agent =  create_agent(
        model = get_job_match_model(),
        tools = [generate_resume],
        system_prompt = GATEKEEPER_AGENT_PROMPT,
        response_format = ProviderStrategy(RewrittenResume), 
        checkpointer = InMemorySaver(),
        middleware = [HumanInTheLoopMiddleware(
            interrupt_on = {
                "generate_resume": {
                    "allowed_decisions": ["approve","reject"],
                }
            }
        )]
        
    )

def gated_agent_check(resume_text: str, job_description: str):
    print("Checking if resume is well-tailored to the job description...")  
    if gated_agent is None:
        create_gated_agent()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    result = gated_agent.invoke({
        "messages":[
            HumanMessage(content=f"Original resume: {resume_text}\n\nJob description: {job_description}")
        ],
       
    }, config = config)
    print("gated agent " , result)
    print(result["messages"][-1].tool_calls)
    for tool_call in result["messages"][-1].tool_calls: 
        if tool_call["name"] == "generate_resume":
            print("Tool call to generate_resume detected. Tool input: ", tool_call["args"])   
    print("Thread ID: ", thread_id)
    return thread_id 

def gated_agent_resume(thread_id: str, decision: str) -> RewrittenResume:
    print(f"User decision for thread {thread_id}: {decision}")
    if gated_agent is None:
        create_gated_agent()
    config = {"configurable": {"thread_id": thread_id}}
    decision = "approve" if decision == "yes" else "reject"
    result = gated_agent.invoke(Command(resume={"decisions":[{"type":decision}]}), config = config)
    print("gated agent resume result " , result.get("structured_response"))
    return result.get("structured_response")