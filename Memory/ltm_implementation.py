# -----------------------------------------------------
# Program-1 : Chatbot Reading Existing Memories
# -----------------------------------------------------


# from langgraph.graph import StateGraph, START, END, MessagesState

# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_core.messages import SystemMessage
# from langchain_core.runnables import RunnableConfig

# from langgraph.store.memory import InMemoryStore
# from langgraph.store.base import BaseStore

# from dotenv import load_dotenv
# load_dotenv()

# # ------------------------------------------------------
# # Create LTM store and seed memory before running the graph
# # ------------------------------------------------------

# store = InMemoryStore()

# user_id = "user1"
# user_details = ("user", user_id, "details")

# store.put(user_details, "profile_1", {"data": "Name: saurabh"})
# store.put(user_details, "profile_2", {"data": "Profession: Software Engineer"})
# store.put(user_details, "preference_1", {"data": "prefer concise answers"})
# store.put(user_details, "preference_2", {"data": "He likes to code in python"})
# store.put(user_details, "project_1", {"data": "Building AI Learning Assistant Chatbot using RAG"})
# store.put(user_details, "project_2", {"data": "Built a AI powered resume analyzer"})
# store.put(user_details, "hobby_1", {"data": "likes to play and watch cricket"})

# # -------------------------------------
# # System prompt Template
# # -------------------------------------
# SYSTEM_PROMPT_TEMPLATE = """ You're helpful AI assistant with memory capabilities.
#     If user-specific memory is available, use it to personalize your responses based on wat you know about the user.

#     Your goal is to provide the relevant, friendly and tailored assistance that reflect the user's preferences, context and past interactions.

#     If user's name or relevant personal context is available , always personalize your responses by:
#         - Always address the user by his name (e.g., Sure, Saurabh...) when appropriate
#         - Referencing known projects, tools, or preferences (e.g., your MCP  server python based project)
#         - Adjusting the tone to feel friendly, natural and directly aimed at the user

#     Avoid  generic phrasing when personalization is possible. For example, instead of "In TypeScript apps..." say "Since your project is built with TypeScript..."

#     Use Personalization especially in :
#         - greeting and transitions
#         - Help or guidance tailored to tools and frameworks the user uses
#         - Follow-up messages that continue from past context

#     Always ensure that personalization is based only on user know details and not assumed.
#     In the end suggest 3 further questions based on the current response and user profile.
#     The user's memory (which may be empty) provided as : {user_details_content}
#     """

# # ----------------------------
# # 3) Build graph: START -> chat -> END (read-only LTM)
# # ----------------------------
# llm = ChatOpenAI(model="gpt-4o-mini")

# def chat_node(state: MessagesState, config:RunnableConfig, store:BaseStore):
#     user_id = config["configurable"]["user_id"]
    
#     user_details = ("user", user_id, "details")
#     items = store.search(user_details)

#     # Convert memory items into a string blob for {user_details_content}
#     if items:
#         user_details_content = "\n".join(f"- {item.value.get("data", '')}" for item in items)
#     else:
#         user_details_content = ""
    
#     system_prompt = SYSTEM_PROMPT_TEMPLATE.format(user_details_content=user_details_content)

#     system_message = SystemMessage(content=system_prompt)
#     response = llm.invoke([system_message] + state["messages"])
#     return {"messages": [response]}

# builder = StateGraph(MessagesState)
# builder.add_node("chat_node", chat_node)
# builder.add_edge(START, "chat_node")
# builder.add_edge("chat_node", END)

# graph = builder.compile(store=store)

# config = {"configurable": {"user_id": "user1"}}
# result = graph.invoke(
#     {"messages": [{"role": "user", "content": "Explain gen ai in simple terms."}]}, config=config
#     )

# print(result["messages"][-1].content)



# -----------------------------------------------------
# Program-2 : Chatbot Creating New Memories
# -----------------------------------------------------



