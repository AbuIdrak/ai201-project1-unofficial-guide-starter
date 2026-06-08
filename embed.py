import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest

def build_vector_store(data_dir="data"):
    # Load and chunk all documents
    chunks = ingest(data_dir)
    
    # Set up embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Set up ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it already exists (clean rebuild)
    try:
        client.delete_collection("unofficial_guide")
    except:
        pass
    
    collection = client.create_collection("unofficial_guide")
    
    # Embed and store chunks
    print(f"Embedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": source} for source in sources]
    )
    
    print(f"Done! {len(chunks)} chunks stored in ChromaDB.")
    return collection

if __name__ == "__main__":
    build_vector_store()