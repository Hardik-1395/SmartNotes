from langchain_community.embeddings import OllamaEmbeddings

def get_embeddings(model_type: "ollama"):
    if model_type == "ollama":
        return OllamaEmbeddings(model="nomic-embed-text")
    else:
        raise ValueError(f"Unknown embedding model: {model_type}")