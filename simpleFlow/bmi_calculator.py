from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Defibne your state
class BMIState(TypedDict):
    height_m:float
    weight_kg:float
    bmi: float
    category:str

# Function to calculate bmi
def calculate_bmi(state:BMIState) -> BMIState:
    weight = state["weight_kg"]
    height = state["height_m"]
    bmi = (weight)/(height**2)
    state["bmi"] = bmi
    return state

# function to define label
def define_label(state: BMIState) -> BMIState:
    bmi = state["bmi"]

    if bmi < 18.5:
        category = "Underweight"
    elif bmi >= 18.5 and bmi < 25:
        category = "Normal"
    elif bmi >= 25 and bmi < 30:
        category = "Overweight"
    else: category = "Obese"

    state["category"] = category
    return state

# DEfine Your graph
graph = StateGraph(BMIState)

# Add node
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node("define_label", define_label)

# Add edges to the node
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "define_label")
graph.add_edge("define_label", END)

# Compile the graph
workflow = graph.compile()

# Execute the graph
initial_state = {"height_m": 1.8, "weight_kg":80}
result = workflow.invoke(initial_state)
print(result)