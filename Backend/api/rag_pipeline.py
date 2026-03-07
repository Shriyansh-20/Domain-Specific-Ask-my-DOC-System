import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama


PERSIST_DIR = "chroma_db"


embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


llm = Ollama(model="llama3")


def process_pdf(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=PERSIST_DIR
    )

    vector_db.persist()



def ask_question(question):

    vector_db = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding
    )

    docs = vector_db.similarity_search(question, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

If the answer is not present in the context say:
"No relevant answer found in the document."
"""

    response = llm.invoke(prompt)

    return response