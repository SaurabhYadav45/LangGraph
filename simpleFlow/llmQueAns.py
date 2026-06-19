from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Load LLM Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key= api_key
)

# Define State
class LLMState(TypedDict):
    question: str
    answer: str

# LLM Question answer
def llm_QA(state: LLMState)-> LLMState:
    que = state["question"]
    prompt = f"Answer the Following question {que}"
    ans = model.invoke(prompt).content
    state["answer"] = ans
    return state

# Define your graph
graph = StateGraph(LLMState)
# Add Nodes
graph.add_node("llm_QA", llm_QA)

# Add Edges
graph.add_edge(START, "llm_QA")
graph.add_edge("llm_QA", END)

# Compile graph
workflow = graph.compile()

# Execute graph
initial_state = {"question": "How far is moon from the earth?"}
result = workflow.invoke(initial_state)
print(result)
