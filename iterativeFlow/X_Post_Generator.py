from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal, Annotated
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
import operator
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key = api_key
)

class TweetEvaluation(BaseModel):
    evaluation:Literal["approved", "need_improvement"] = Field(..., description="Final evaluation result")
    feedback:str = Field(..., description="Feedback for the tweet")

structured_model = model.with_structured_output(TweetEvaluation)

class TweetState(TypedDict):
    topic:str
    tweet:str
    evaluation:Literal["approved", "need_improvemnt"]
    feedback:str
    iteration:int
    max_iteration:int

    tweet_history: Annotated[list[str], operator.add]
    feedback_history: Annotated[list[str], operator.add]


def generate_tweet(state:TweetState):
    topic = state["topic"]
    messages = [
        SystemMessage(content="You're a clever, funny and sarcastic Twitter/X influencer."),
        HumanMessage(content=f"""Write a short, original and hilarious tweet on the topic: "{topic}"
        Rules:
        - Do NOT use question-answer format.
        - Max 280 characters.
        - Use observational humor, irony, sarcasm, or cultural references.
        - Think in meme logic, punchlines, or relatable takes.
        - Use simple, day to day english.
        """)
    ]
    tweet = model.invoke(messages).content
    return {"tweet": tweet, "tweet_history": [tweet]}

def evaluate_tweet(state:TweetState):
    messages = [
        SystemMessage(content="You're a ruthless, no-laugh-given twitter/X critic. You evaluate tweet based on humor, originality, virality and tweet format."),
        HumanMessage(content=f"""
        Evaluate the following tweet:

Tweet: "{state['tweet']}"

Use the criteria below to evaluate the tweet:

1. Originality – Is this fresh, or have you seen it a hundred times before?  
2. Humor – Did it genuinely make you smile, laugh, or chuckle?  
3. Punchiness – Is it short, sharp, and scroll-stopping?  
4. Virality Potential – Would people retweet or share it?  
5. Format – Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)?

Auto-reject if:
- It's written in question-answer format (e.g., "Why did..." or "What happens when...")
- It exceeds 280 characters
- It reads like a traditional setup-punchline joke
- Dont end with generic, throwaway, or deflating lines that weaken the humor (e.g., “Masterpieces of the auntie-uncle universe” or vague summaries)

### Respond ONLY in structured format:
- evaluation: "approved" or "needs_improvement"  
- feedback: One paragraph explaining the strengths and weaknesses 
""")
    ]

    response = structured_model.invoke(messages)
    return {"evaluation": response.evaluation, "feedback":response.feedback, "feedback_history": [response.feedback]}


def optimize_tweet(state:TweetState):
    messages = [
        SystemMessage(content="You punch up tweet for virality and humor based on given feedback."),
        HumanMessage(content=f"""
        Improve the tweet based on this feedback:
        "{state["feedback"]}"
        Topic: "{state["topic"]}"
        original tweet: "{state["tweet"]}"

        Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.
""")
    ]

    response = model.invoke(messages).content
    iteration = state["iteration"] + 1
    return {"tweet": response, "iteration":iteration, "tweet_history":[response]}

def route_evaluation(state:TweetState):
    evaluation = state["evaluation"]
    iteration = state["iteration"]
    max_iteration = state["max_iteration"]

    if evaluation == "approved" or iteration >= max_iteration:
        return "approved"
    else:
        return "need_improvement"

graph = StateGraph(TweetState)

graph.add_node("generate_tweet", generate_tweet)
graph.add_node("evaluate_tweet", evaluate_tweet)
graph.add_node("optimize_tweet", optimize_tweet)

graph.add_edge(START, "generate_tweet")
graph.add_edge("generate_tweet", "evaluate_tweet")
graph.add_conditional_edges("evaluate_tweet", route_evaluation, {"approved": END, "need_improvement": "optimize_tweet"})
graph.add_edge("optimize_tweet", "evaluate_tweet")

# compile graph
workflow = graph.compile()

# Execute graph
initial_state = {
    "topic":"Exam paper leak",
    "iteration":1,
    "max_iteration":5
}

result = workflow.invoke(initial_state)

print(result["topic"])
print(result["tweet"])
print(result["evaluation"])
print(result["feedback"])
print(result["iteration"])
print(result["max_iteration"])
print(result["tweet_history"])
print(result["feedback_history"])