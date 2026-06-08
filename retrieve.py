import chromadb
from sentence_transformers import SentenceTransformer

N_RESULTS = 7

_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_collection("unofficial_guide")
_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, n_results=N_RESULTS):
    # Embed the query and search ChromaDB
    query_embedding = _model.encode([query]).tolist()
    
    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    # ChromaDB returns nested lists — [0] gets results for our single query
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    
    # Return empty list if nothing found
    if not documents:
        return []
    
    return [
        {
            "text": documents[i],
            "source": metadatas[i]["source"],
            "distance": distances[i]
        }
        for i in range(len(documents))
    ]

if __name__ == "__main__":
    # Test with your evaluation questions
    test_queries = [
        "What do students say about how many clothes to bring to a dorm?",
        "What habits should freshmen stop doing in class?",
        "What should I look for when choosing a laptop on a budget?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retrieve(query)
        for r in results:
            print(f"  Source: {r['source']} | Distance: {r['distance']:.3f}")
            print(f"  Text: {r['text'][:100]}...")
        print("-" * 60)