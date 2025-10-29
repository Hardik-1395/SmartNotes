from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.create_documents([text])
