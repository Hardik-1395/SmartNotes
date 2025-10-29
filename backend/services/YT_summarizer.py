# TODO
# IMPLEMENT RATE LIMITING TO AVOID QUOTA ERRORS 
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from pydantic import SecretStr
import re

load_dotenv()
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")

model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
llm = ChatGroq(model=model_name, api_key=SecretStr(GROQ_API_KEY) if GROQ_API_KEY else None)

prompt_template = """
You are an expert content summarizer. Your task is to produce a clear, accurate, and token-efficient summary of the content below.

Requirements:
- Language: **English only**.
- Maximum length: **400 words**.
- Style: Clear, concise, explanatory (as if teaching), using short direct sentences.
- Coverage: Capture only the main ideas and essential details. 
- Efficiency: Avoid repetition, filler words, or restating the same idea in different forms.
- Faithfulness: Do not add new information, assumptions, or opinions.
- Audience: Assume the reader is learning the topic and wants a precise explanation.

Content to summarize:
{text}

Final Summary:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

CHUNK_SIZE = 5000 

def format_markdown_bold(text: str) -> str:
    """Convert markdown-style bold (**text**) into styled HTML."""
    formatted = re.sub(r"\*\*(.*?)\*\*", r'<span class="section-title">\1</span>', text)
    formatted = formatted.replace("\n", "<br>")
    return formatted

def chunk_transcript(transcripts: list[dict], chunk_size=CHUNK_SIZE) -> list[str]:
    """Turn transcript list of dicts into word chunks (strings)."""
    full_text = " ".join([line["text"] for line in transcripts])  # <-- ensure pure string
    words = full_text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def summarize_youtube_video(text: str) -> str:
    """Summarize a single chunk of text."""
    try:
        if not text.strip():
            return "No content found for the provided YouTube URL."

        docs = [Document(page_content=text)]  # <-- must be a string
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
        summary = chain.run(docs)
        return summary.strip()
    except Exception as e:
        return f"Failed to summarize video: {str(e)}"

def summarize_long_transcript(transcripts: list[dict]) -> str:
    """Handle long transcripts by chunking + combining summaries."""
    chunks = chunk_transcript(transcripts)
    chunk_summaries = [summarize_youtube_video(chunk) for chunk in chunks]

    final_summary = summarize_youtube_video(" ".join(chunk_summaries))
    return final_summary
