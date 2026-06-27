# ************ Type-2 : Add a subgraph as a Node ***************************

# ******************** Example: 2 **********************
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

# Define subgraph
class SubgraphState(TypedDict):
    foo: str  # shared with parent graph state
    bar: str  # private to SubgraphState

def subgraph_node_1(state: SubgraphState):
    return {"bar": "bar"}

def subgraph_node_2(state: SubgraphState):
    # note that this node is using a state key ('bar') that is only available in the subgraph
    # and is sending update on the shared state key ('foo')
    return {"foo": state["foo"] + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# Define parent graph
class ParentState(TypedDict):
    foo: str

def node_1(state: ParentState):
    return {"foo": "hi! " + state["foo"]}

builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", subgraph)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
graph = builder.compile()

stream = graph.stream_events({"foo": "foo"}, version="v3")
for event in stream:
    if event["method"] == "updates" and not event["params"]["namespace"]:
        print(event["params"]["data"])

#  ******************* Example : 1 *********************

# from typing_extensions import TypedDict
# from langgraph.graph.state import StateGraph, START

# class State(TypedDict):
#     foo: str

# # Subgraph

# def subgraph_node_1(state: State):
#     return {"foo": "hi! " + state["foo"]}

# subgraph_builder = StateGraph(State)
# subgraph_builder.add_node(subgraph_node_1)
# subgraph_builder.add_edge(START, "subgraph_node_1")
# subgraph = subgraph_builder.compile()

# # Parent graph

# builder = StateGraph(State)
# builder.add_node("node_1", subgraph)
# builder.add_edge(START, "node_1")
# graph = builder.compile()