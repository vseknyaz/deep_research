from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import os
from langsmith import traceable

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "my-research-agent"

# Initialize LLM outside the node
llm = ChatOpenAI(model="gpt-4", temperature=0.0)

# Define the state schema
class DeepResearchState(TypedDict):
    goal: str
    sub_questions: list[str]
    manager_messages: Annotated[list[BaseMessage], add_messages]

# Planner Node
@traceable
def planner_node(state: DeepResearchState) -> DeepResearchState:
    # Access goal from state
    goal = state["goal"]
    prompt = PromptTemplate.from_template("""
    Break this research goal into 3-5 sub-questions. 
    Return ONLY a JSON array: ["query1", "query2", ...]
    Goal: {goal}
    """)
    response = llm.invoke(prompt.format(goal=goal))
    return {"sub_questions": eval(response.content)}  # Return only updated fields

# Build and Compile Graph
workflow = StateGraph(DeepResearchState)
workflow.add_node("planner", planner_node)
workflow.add_edge(START, "planner")
workflow.add_edge("planner", END)  # Ensure graph terminates

# Compile the executable graph
graph = workflow.compile()

# Test the graph
# if __name__ == "__main__":
#     result = graph.invoke({"goal": "Techniques for compressing LLMs under 1B parameters"})
#     print(result["sub_questions"])