from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = api_key
)

# 1.
@tool
def get_stock_price(symbol:str)->dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()

# 2.
search_tool = DuckDuckGoSearchRun(region="us-en")

# 3.
@tool
def calculator(first_num: float, second_num: float, operation: str)->dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage], add_messages]

# Make tool list
tools = [get_stock_price, search_tool, calculator]

# Make the llm tool aware
llm_with_tools = model.bind_tools(tools)

def chat_node(state:ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools(messages)
    return {"messages": [response]}

# tool Node
tool_node = ToolNode(tools)

# Initialize graph
graph = StateGraph(ChatState)

# Add Nodes
graph.add_node("chat_node", chat_node)
graph.add_node("tool_node", tool_node)

# Add edges
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tool_node", "chat_node")

# Compile Graph
chatbot = graph.compile()

# Invoke graph
chatbot.invoke({"messages": [HumanMessage(content="hello!")]})