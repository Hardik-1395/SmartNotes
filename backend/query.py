import argparse
import os
from typing import List

from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


DEFAULT_PERSIST_DIR = "./vectorstores"
DEFAULT_MODEL = "llama-3.1-70b-versatile"  # Alternatives: "llama-3.1-8b-instant", "mixtral-8x7b-32768"


def _resolve_embeddings():
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if google_api_key and GoogleGenerativeAIEmbeddings is not None:
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    

def _resolve_llm(model_name: str):
    if ChatGroq is None:
        raise RuntimeError(
            "langchain-groq is not installed. Install it and set GROQ_API_KEY."
        )
    if not os.getenv("GROQ_API_KEY"):
        raise EnvironmentError("GROQ_API_KEY not found in environment.")
    return ChatGroq(model=model_name, temperature=0)


def _build_prompt() -> PromptTemplate:
    template = (
        "You are a helpful AI assistant. Use the provided context to answer the question.\n"
        "If the answer cannot be derived from the context, say you don't know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
    return PromptTemplate(template=template, input_variables=["context", "question"])


def main():
    parser = argparse.ArgumentParser(
        description="Query a Chroma vector store collection using a Groq LLM."
    )
    parser.add_argument(
        "--collection",
        type=str,
        required=True,
        help="Collection name under persist directory.",
    )
    parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="User question for contextual Q&A.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=4,
        help="Number of relevant chunks to retrieve (default: 4).",
    )
    parser.add_argument(
        "--persist_dir",
        type=str,
        default=DEFAULT_PERSIST_DIR,
        help="Base directory where vector collections are stored.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="Groq LLM model name (e.g., llama-3.1-70b-versatile, mixtral-8x7b-32768).",
    )
    args = parser.parse_args()

    embeddings = _resolve_embeddings()
    llm = _resolve_llm(args.model)
    collection_path = os.path.join(args.persist_dir, args.collection)

    vectorstore = Chroma(
        persist_directory=collection_path,
        collection_name=args.collection,
        embedding_function=embeddings,
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": args.k})

    prompt = _build_prompt()
    answer_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    rag_with_sources = RunnableParallel(
        answer=answer_chain,
        context=retriever,
    )
    result = rag_with_sources.invoke(args.question)

    print("\nAnswer:")
    print((result.get("answer", "") or "").strip())
    sources = result.get("context", []) or []
    if sources:
        print("\nSources:")
        for i, doc in enumerate(sources, 1):
            meta = getattr(doc, "metadata", {}) or {}
            page_content = getattr(doc, "page_content", "") or ""
            snippet = page_content[:200].replace("\n", " ")
            print(f"[{i}] {meta.get('source', 'N/A')} :: {snippet}...")


if __name__ == "__main__":
    main()


