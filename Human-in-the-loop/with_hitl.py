from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
# Himan in the Loop
from langgraph.types import interrupt, Command

from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from dotenv import load_dotenv
import os
import requests

load_dotenv()

# LLM

# api_key = os.getenv("GEMINI_API_KEY")
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=api_key
# )

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=api_key
)

# -------------------
# 2. Tools
# -------------------
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    )
    r = requests.get(url)
    return r.json()


@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
    Simulate purchasing a given quantity of a stock symbol.

    HUMAN-IN-THE-LOOP:
    Before confirming the purchase, this tool will interrupt and wait for a human decision("yes"/ Anything else)
    
    """
    decision = interrupt(f"Approve buying {quantity} shares of {symbol}? (yes/no)")
    print(repr(decision))

    if isinstance(decision, str) and decision.lower() == "yes":
        return {
            "status": "success",
            "message": f"Purchase order placed for {quantity} shares of {symbol}.",
            "symbol": symbol,
            "quantity": quantity,
        }
    else:
        return{
            "status": "Cancelled",
            "message":f"Purchase of {quantity} shares of {symbol} was declined by human",
            "symbol":symbol,
            "quantity":quantity
        }


tools = [get_stock_price, purchase_stock]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

graph = StateGraph(State)


def chatnode(state:State):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

graph.add_node("chatnode", chatnode)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chatnode")
graph.add_conditional_edges("chatnode", tools_condition)
graph.add_edge("tools", "chatnode")

checkpointer = InMemorySaver()

chatbot = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    print("Stock bot with tools (get_stock_price, purchase_stock)")
    print("type 'exit' to quit \n")

    config = {"configurable": {"thread_id": "thread-2"}}

    while True:
        user_input = input("Enter your query:")
        if user_input.lower().strip() in {"exit", "quit"}:
            print("GoodBye!")
            break

        initial_state = [HumanMessage(content=user_input)]

         # Run the graph (may hit an interrupt)
        result = chatbot.invoke({"messages":initial_state}, config=config)

        # Check for HITL interrupt from Purchase stock
        interrupts = result.get("__interrupt__", [])
        

        if interrupts:
            prompt_to_human = interrupts[0].value
            print(f"HITL: {prompt_to_human}")
            decision = input("Your decision: ").lower().strip()
            # Resume graph with the human decision ("yes" / "no" / whatever)
            result = chatbot.invoke(
                Command(resume=decision),
                config=config
            )

         # Get the latest message from the assistant
        messages = result["messages"]
        last_msg = messages[-1]
        print(f"Bot: {last_msg.content}\n")
