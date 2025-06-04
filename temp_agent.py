from langgraph.graph import StateGraph  # Changed from Graph to StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import os
from langsmith import traceable  # Decorate nodes
from langgraph.graph import END, START, StateGraph


load_dotenv()

# Then set up LangSmith
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # From .env file
# os.environ["LANGCHAIN_PROJECT"] = "my-research-agent"  # Optional project name
llm = ChatOpenAI(model="gpt-4", temperature=0.0)

class DeepResearchState(TypedDict):
    manager_messages: Annotated[list[BaseMessage], add_messages]

# 2. Planner Node
def planner_node(state: dict):
    goal = state["goal"]
    prompt = PromptTemplate.from_template("""
    Break this research goal into 3-5 sub-questions. 
    Return ONLY a JSON array: ["query1", "query2", ...]
    Goal: {goal}
    """)
    response = llm.invoke(prompt.format(goal=goal))
    return {"sub_questions": eval(response.content)}

# 3. Build and Compile Graph
workflow = StateGraph(DeepResearchState)  # Initialize with state type (dict)
workflow.add_node("planner", planner_node)
workflow.add_edge(START, "planner")

graph = workflow.compile()  # Compile the executable

# # 4. Test
# result = graph.invoke({"goal": "Techniques for compressing LLMs under 1B parameters"})
# print(result["sub_questions"])