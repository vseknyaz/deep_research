from langgraph.graph import StateGraph  # Changed from Graph to StateGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langsmith import traceable  # Decorate nodes


load_dotenv()

# Then set up LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # From .env file
os.environ["LANGCHAIN_PROJECT"] = "my-research-agent"  # Optional project name
llm = ChatOpenAI(model="gpt-4", temperature=0.0)

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
workflow = StateGraph(dict)  # Initialize with state type (dict)
workflow.add_node("planner", planner_node)
workflow.set_entry_point("planner")
workflow.set_finish_point("planner")  # Temporary for single-node graph

app = workflow.compile()  # Compile the executable

# 4. Test
if __name__ == "__main__":
    result = app.invoke({"goal": "Techniques for compressing LLMs under 1B parameters"})
    print(result["sub_questions"])