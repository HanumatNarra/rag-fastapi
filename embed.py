import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("documents")

with open("my_info.txt", "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["my_info"])

print("Embedding stored in Chroma")