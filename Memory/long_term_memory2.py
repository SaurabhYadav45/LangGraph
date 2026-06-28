from langgraph.store.memory import InMemoryStore

# Create a store
store = InMemoryStore()

# Create a namespace and memories
namespace = ("user", "user1")

# store.put(namespace, key, value)
store.put(namespace, "1", {"data": "User likes Pizza"})
store.put(namespace, "2", {"data": "user prefers dark mode"})

namespace2 = ("user", "user2")
store.put(namespace2, "1", {"data": "User prefers pasta"})
store.put(namespace2, "2", {"data": "User prefers grid like navigation"})

# Print store:
print(store)

# Retrieving Memories
# store.get(namespace, key)
item1 = store.get(namespace2, "1")
item2 = store.get(namespace2, "2")
# print(item1)
# print(item2)
print("item1: ",item1.value)
print("Item2: ",item2.value)

# Retrieving All Memories
items = store.search(namespace)
for item in items:
    # print(item)
    print(item.value)



# Method : 2 => Semantic search

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')
store = InMemoryStore(index={"embed":embedding_model, "dims": 1536})

namespace3 = ("user", "user3")
store.put(namespace3, "1", {"data": "User prefers concise answers over long explanations"})
store.put(namespace3, "2", {"data": "User likes examples in Python"})
store.put(namespace3, "3", {"data": "User usually works late at night"})
store.put(namespace3, "4", {"data": "User prefers dark mode in applications"})
store.put(namespace3, "5", {"data": "User is learning machine learning"})
store.put(namespace3, "6", {"data": "User dislikes overly theoretical explanations"})
store.put(namespace3, "7", {"data": "User prefers step-by-step reasoning"})
store.put(namespace3, "8", {"data": "User is based in India"})
store.put(namespace3, "9", {"data": "User likes real-world analogies"})
store.put(namespace3, "10", {"data": "User prefers bullet points over paragraphs"})

items = store.search(namespace3, query="what is the user currently learning", limit=3)
print("query1: what is the user currently learning")
for item in items:
    print(item.value)

print("\n")
items = store.search(namespace3, query="what are user's preferences", limit=3)
print("query2: what are user's preferences")
for item in items:
    print(item.value)

