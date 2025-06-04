# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langsmith import traceable
#
# # Initialize LLM (move to agent.py if shared)
# llm = ChatOpenAI(model="gpt-4", temperature=0.0)
#
# @traceable
# def planner_node(state: dict) -> dict:
#     prompt = PromptTemplate.from_template("""
#     Break this research goal into 3-5 sub-questions.
#     Return ONLY a JSON array: ["query1", "query2", ...]
#     Goal: {goal}
#     """)
#     response = llm.invoke(prompt.format(goal=state["goal"]))
#     state["sub_questions"] = eval(response.content)
#     return state