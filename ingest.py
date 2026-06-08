import os

def load_documents(data_dir="data"):
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text
            })
    return documents

def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

def ingest(data_dir="data"):
    documents = load_documents(data_dir)
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i
            })
    return all_chunks

if __name__ == "__main__":
    chunks = ingest()
    print(f"Total chunks: {len(chunks)}")
    print("\n--- 5 sample chunks ---")
    for chunk in chunks[:5]:
        print(f"\nSource: {chunk['source']}")
        print(f"Text: {chunk['text']}")
        print("-" * 40)