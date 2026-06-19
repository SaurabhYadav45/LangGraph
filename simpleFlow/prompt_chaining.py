from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
import os

# load env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
# load model
model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = api_key
)

# define state
class BlogState(TypedDict):
    topic:str
    outline:str
    content:str

# func to create outline
def generate_outline(state: BlogState) ->BlogState:
    topic = state["topic"]
    prompt = f" Generate a detailed outline for the blog for given topic {topic}"
    outline = model.invoke(prompt).content
    state["outline"] = outline
    return state

def generate_contnet(state: BlogState) -> BlogState:
    topic = state["topic"]
    outline = state["outline"]
    prompt = f" Generate a blog on the topic {topic} using following outline {outline}"
    content = model.invoke(prompt).content
    state["contnet"] = content
    return state

# define graph
graph = StateGraph(BlogState)

# Add nodes
graph.add_node("generate_outline", generate_outline)
graph.add_node("generate_contnet", generate_contnet)

# Add edges
graph.add_edge(START, "generate_outline")
graph.add_edge("generate_outline", "generate_contnet")
graph.add_edge("generate_contnet", END)

# Compile graph
workflow = graph.compile()

# execute the graph
initial_state = {"topic": "Rise of AI in India"}
result = workflow.invoke(initial_state)
# print(result)
print(result["topic"])
print(result["outline"])
print(result["content"])

