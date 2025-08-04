import getpass
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

tool = TavilySearch(max_results=2)
tools = [tool]
response = tool.invoke("Who is Rohit sharma")
print("Response:\n", response['results'][0])



