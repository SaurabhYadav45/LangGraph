from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv["GEMINI_API_KEY"]
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = api_key
)

# Define State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chatbot(state:State):
    messages = state["messages"]
    response = model.invoke(messages).content
    return {"messages": [response]}

# define graph
graph = StateGraph(State)

# Add Nodes
graph.add_node("chatbot", chatbot)

# Add Edge
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# compile the graph
workflow = graph.compile()

# Invoke the graph
initial_state = {
    'messages': [HumanMessage(content='What is the capital of india')]
}
workflow.invoke(initial_state)["messages"][-1].content