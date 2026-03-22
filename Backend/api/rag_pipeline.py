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


def process_pdf(file_path, session_id):
    existing_files = os.listdir(f"sessions/{session_id}/docs")
    if os.path.basename(file_path) in existing_files:
        print("File already processed")
        return

    persist_dir = f"sessions/{session_id}/chroma_db"

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

    chunks = splitter.split_documents(documents)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=persist_dir
    )

    print("Vector DB created and persisted at:", persist_dir)

    vector_db.persist()

    print("Loaded documents:", len(documents))
    print("Chunks created:", len(chunks))



def ask_question(question, session_id):
    print(f"Processing question: {question} for session: {session_id}")
    persist_dir = f"sessions/{session_id}/chroma_db"
    vector_db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding
    )
    print("Vector database loaded successfully.")
    results = vector_db.similarity_search_with_score(question, k=3)
    print(f"Retrieved {len(results)} results from vector database.")
    # docs = vector_db.similarity_search(question, k=3)
    # print("Docs retrieved:", len(docs))
    filtered_docs = []
    for doc, score in results:
        if score < 10:   # lower = better match (important!)
            print("Score: ", score)
            filtered_docs.append(doc)
        else :
            print("Score: ", score)


    print(f"Found {len(filtered_docs)} relevant documents after filtering.")
    if not filtered_docs:
        return {
            "answer": "No relevant information found in the document.",
            "sources": []
        }

    context = "\n".join([doc.page_content for doc in filtered_docs])

    unique_sources = set()
    sources = []

    for doc in filtered_docs:
        source = os.path.basename(doc.metadata.get("source", "Unknown document"))
        page = doc.metadata.get("page", 0) + 1

        key = (source, page)

        if key not in unique_sources:
            unique_sources.add(key)

            sources.append({
                "document": source,
                "page": page
            })

    prompt = f"""
You are a strict document assistant.

Answer ONLY using the provided context.

If the answer is not clearly present, say:
"No relevant information found in the document."

Be concise and accurate.

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
    "answer": response,
    "sources": sources
}