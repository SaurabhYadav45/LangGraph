from typing import TypedDict
from langgraph.graph import START, END, StateGraph
import pprint

class State(TypedDict):
    runs:int
    balls:int
    fours:int
    sixes:int
    strikeRate:float
    boundary_percent:float
    ball_per_boundary:float
    summary:str


def calculate_strikeRate(state:State):
    sr = (state['runs']/state['balls'])*100
    return {'strikeRate':sr}

def calculate_boundary_percent(state:State):
    boundary_percent = (state['runs']/(state['fours'] + state['sixes']))*100
    return {'boundary_percent':boundary_percent}

def calculate_ball_per_boundary(state:State):
    ball_per_boundary = ((state['fours']*4 + state['sixes']*6)/state['runs'])
    return {'ball_per_boundary':ball_per_boundary}

def calculate_summary(state:State):
    summary = f"""
Strike rate : {state['strikeRate']}\n
Balls Per Boundary : {state['ball_per_boundary']}\n
Boundary Percentage : {state['boundary_percent']}\n
"""
    return {'summary':summary}


# Add nodes

graph_builder = StateGraph(State)


graph_builder.add_node("calculate_strikeRate", calculate_strikeRate)
graph_builder.add_node("calculate_boundary_percent", calculate_boundary_percent)
graph_builder.add_node("calculate_ball_per_boundary", calculate_ball_per_boundary)
graph_builder.add_node("calculate_summary", calculate_summary)

# Add Edges

graph_builder.add_edge(START, "calculate_strikeRate")
graph_builder.add_edge(START, "calculate_boundary_percent")
graph_builder.add_edge(START, "calculate_ball_per_boundary")

graph_builder.add_edge("calculate_strikeRate", "calculate_summary")
graph_builder.add_edge("calculate_boundary_percent", "calculate_summary")
graph_builder.add_edge("calculate_ball_per_boundary", "calculate_summary")

graph_builder.add_edge("calculate_summary", END)

# compile
graph = graph_builder.compile()


# Invoke the graph
initial_state = {
    'runs': 100,
    'balls': 50,
    'fours': 6,
    'sixes': 4
}
result = graph.invoke(initial_state)
# print("Final result: \n", result)
pprint.pprint(result)
