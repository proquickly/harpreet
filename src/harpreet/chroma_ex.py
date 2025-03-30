import chromadb
import pprint

print = pprint.pprint

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="my_collection")

collection.upsert(
    documents=[
        "a guide to touring vineyards in france",
        "a book on portugal",
        "visit russia",
        "see penguins",
        "in mexico they speak spanish"
    ],
    ids=["id1", "id2", "id3", "id4", "id5"]
)

results = collection.query(
    query_texts=["who wears a sombrero"],
    n_results=2
)

print(results)
