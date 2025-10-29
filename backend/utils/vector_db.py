import os
from langchain_community.vectorstores import FAISS

BASE_DIR = "vectorstores"  # All indexes stored here

def create_vector_store(docs, embeddings, store_name):
    """Create a new FAISS vector store and save it under a unique name."""
    os.makedirs(BASE_DIR, exist_ok=True)
    vectorstore = FAISS.from_documents(docs, embeddings)
    save_path = os.path.join(BASE_DIR, f"{store_name}.faiss")
    vectorstore.save_local(save_path)
    return vectorstore


def load_vector_store(store_name, embeddings):
    """Load a specific FAISS vector store by its name."""
    save_path = os.path.join(BASE_DIR, f"{store_name}.faiss")
    if not os.path.exists(save_path):
        raise FileNotFoundError(f"No vector store found for {store_name}")
    return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)


def list_vector_stores():
    """List all saved vector stores."""
    if not os.path.exists(BASE_DIR):
        return []
    return [f.replace(".faiss", "") for f in os.listdir(BASE_DIR) if f.endswith(".faiss")]


def delete_vector_store(store_name):
    """Remove a stored FAISS index."""
    save_path = os.path.join(BASE_DIR, f"{store_name}.faiss")
    if os.path.exists(save_path):
        os.remove(save_path)
