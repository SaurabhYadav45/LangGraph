from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
# from openai import OpenAI
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

#  LLM
llm = init_chat_model("openai:gpt-4.1")

def chatbot(state:State):
    response = {"messages":[llm.invoke(state["messages"])]}
    print("Response:", response)
    return response

# Add Nodes
graph_builder.add_node("chatbot", chatbot)

# Add Edge
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# compile the graph
graph = graph_builder.compile()

# Invoke the graph
query = {"messages":["Hi I'm Saurabh"]}
graph.invoke(query)