def build_rag_index(raw_text, summary_text=None, model_type="ollama", store_name=None):
    embeddings = get_embeddings(model_type)

    combined_text = raw_text
    if summary_text:
        combined_text += "\n\nSummary:\n" + summary_text

    docs = chunk_text(combined_text)
    vectorstore = create_vector_store(docs, embeddings, store_name)
    retriever = get_retriever(vectorstore)
    return retriever
