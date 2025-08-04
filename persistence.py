from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from typing import TypedDict
from dotenv import load_dotenv

from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()
llm = ChatOpenAI()

class State(TypedDict):
    topic: str
    joke: str
    explanation: str

def generate_joke(state:State):
    prompt = f""" Generate a joke on the given topic {state["topic"]} """
    response = llm.invoke(prompt).content
    return {"joke": response}


def generate_explanation(state: State):
    prompt = f""" write an small explanation for the given joke  {state["joke"]}"""
    response = llm.invoke(prompt).content
    return {"explanation":response}


graph = StateGraph(State)

graph.add_node("generate_joke", generate_joke)
graph.add_node("generate_explanation", generate_explanation)

graph.add_edge(START, "generate_joke")
graph.add_edge("generate_joke", "generate_explanation")
graph.add_edge("generate_explanation", END)


checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)
config1 = {"configurable":{"thread_id":"1"}}

result = workflow.invoke({"topic": "cricket"}, config=config1)
print("Result:\n", result)


res = workflow.get_state(config=config1)
print("\nres:", res)

res2 = workflow.get_state_history(config1)
print("\nRes2:")
for snapshot in  res2:
    print("\n1:", snapshot)
