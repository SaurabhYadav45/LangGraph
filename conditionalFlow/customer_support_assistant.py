from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# Load LLM model
api_key = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = api_key
)

# Define Sentiment Schema
class SentimentSchema(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(description='Sentiment of the review')

# define schema for structured diagnosis output
class DiagnosisSChema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
    urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be')

# Structure Model
structure_model1 = model.with_structured_output(SentimentSchema)
structure_model2 = model.with_structured_output(DiagnosisSChema)

# Define State
class ReviewState(TypedDict):
    review:str
    sentiment:Literal["positive", "negative"]
    diagnosis:dict
    response:str

# Find sentiment of customer review
def find_sentiment(state:ReviewState):
    review = state["review"]
    prompt = f"Analyze and find the sentiment of the given review or comment \n {review}"
    sentiment = structure_model1.invoke(prompt).sentiment
    return {"sentiment": sentiment}

def check_sentiments(state:ReviewState) ->Literal["run_diagnosis", "positive_response"]:
    sentiment = state["sentiment"]
    if sentiment == "positive":
        return "positive_response"
    else:
        return "run_diagnosis"

# Return response on basis of positive review
def positive_response(state:ReviewState):
    review = state['review']
    prompt = f"Write a warm Thank you message in response to this review. \n {review} \n  Also kindly ask the user to leave a feedbackon our website."
    response = model.invoke(prompt).content
    return {"response": response}

def run_diagnosis(state:ReviewState):
    review = state["review"]
    prompt = f""" Diagnose this negative review \n \n {review} \n Return out the issue_type, tone and urgency """
    response = structure_model2.invoke(prompt)
    return {"diagnosis": response.model_dump()}

def negative_response(state:ReviewState):
     diagnosis = state['diagnosis']
     prompt = f"""You are a support assistant.
The user had a '{diagnosis['issue_type']}' issue, sounded '{diagnosis['tone']}', and marked urgency as '{diagnosis['urgency']}'.
Write an empathetic, helpful resolution message.
"""
     response = model.invoke(prompt).content
     return {"response": response}

# Define graph
graph = StateGraph(ReviewState)

# Add nodes
graph.add_node("find_sentiment", find_sentiment)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)

# Add edges
graph.add_edge(START, "find_sentiment")
graph.add_conditional_edges("find_sentiment", check_sentiments)

graph.add_edge("positive_response", END)
graph.add_edge("run_diagnosis", "negative_response")
graph.add_edge("negative_response", END)

# Compile graph
workflow = graph.compile()

# Execute graph
initial_state = {
    "review" : "The in-depth analysis of course is missing, It might have been much better."
}
result = workflow.invoke(initial_state)
# print(result)
print("Review:", result["review"])
print("Sentiment:", result["sentiment"])
print("Diagnosis:", result["diagnosis"])
print("Response:", result["response"])

