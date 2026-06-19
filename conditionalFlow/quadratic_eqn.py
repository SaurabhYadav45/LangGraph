from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

# Define Graph state
class QuadraticState(TypedDict):
    a:int
    b:int
    c:int
    equation:str
    discriminant:float
    result:str

def show_equation(state:QuadraticState):
    equation = f"{state["a"]}x^2 + {state["b"]}x + {state["c"]}"
    return {"equation": equation}

def find_discriminant(state:QuadraticState):
    a = state["a"]
    b = state["b"]
    c = state["c"]
    discriminant = (b**2) - (4*a*c)
    return {"discriminant":discriminant}

def real_roots(state:QuadraticState):
    a = state["a"]
    b = state["b"]
    d = state["discriminant"]
    root1 = (-b + (d**0.5))/(2*a)
    root2 = (-b - (d**0.5))/(2*a)
    result = f"The roots are {root1} and {root2}"
    return {"result": result}

def repeated_roots(state:QuadraticState):
    a = state["a"]
    b = state["b"]
    root = (-b)/(2*a)
    result = f"The only root is {root}"
    return {"result": result}

def no_real_roots(state:QuadraticState):
    result = "There is no real roots"
    return {"result": result}

def check_condition(state:QuadraticState) -> Literal["real_roots", "repeated_roots", "no_real_roots"]:
    discriminant = state["discriminant"]
    if discriminant > 0:
        return "real_roots"
    elif discriminant == 0:
        return "repeated_roots"
    else:
        return "no_real_roots"
    

# Define Graph
graph = StateGraph(QuadraticState)

# Add nodes
graph.add_node("show_equation", show_equation)
graph.add_node("find_discriminant", find_discriminant)
graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)

# add Edges
graph.add_edge(START, "show_equation")
graph.add_edge("show_equation", "find_discriminant")
graph.add_conditional_edges("find_discriminant", check_condition)

graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)

# Compile graph
workflow = graph.compile()

# Execute Graph
initial_state = {
    "a":2,
    "b":4,
    "c":2
}
result = workflow.invoke(initial_state)
print(result)