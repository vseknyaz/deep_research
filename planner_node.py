import os
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import Graph

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 1. Configure the LLM wrapper
llm = OpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-4o-mini",  # or whichever model you prefer
    temperature=0.0,            # lower temperature for more deterministic plans
)
