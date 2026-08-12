import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_DIR = os.path.join(os.path.dirname(__file__), "..", ".chromadb")
COLLECTION_NAME = "agen_codebase"

from dotenv import load_dotenv

def get_embeddings():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        home_env = os.path.expanduser("~/.agent_env")
        if os.path.exists(home_env):
            load_dotenv(dotenv_path=home_env, override=True)
            api_key = os.getenv("GEMINI_API_KEY")
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if not api_key and os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path, override=True)
            api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured!")
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2", google_api_key=api_key)

def get_vectorstore():
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIR
    )

def index_directory(directory_path: str):
    supported_extensions = [".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ps1"]
    documents = []
    metadatas = []
    
    # Walk through the directory and read files
    for root, _, files in os.walk(directory_path):
        # skip hidden dirs and common heavy dirs
        if any(part.startswith('.') or part in ('venv', 'node_modules', '__pycache__', 'dist', 'build') for part in root.split(os.sep)):
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        documents.append(text)
                        metadatas.append({"source": file_path})
                except Exception:
                    continue

    if not documents:
        return 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.create_documents(documents, metadatas=metadatas)
    
    vectorstore = get_vectorstore()
    vectorstore.add_documents(split_docs)
    
    return len(split_docs)

def get_rag_context(query: str, top_k: int = 5) -> str:
    try:
        if not os.path.exists(DB_DIR):
            return ""
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(query, k=top_k)
        if not results:
            return ""
            
        context = "Relevant Codebase Context (from RAG):\n"
        for doc in results:
            context += f"--- {doc.metadata.get('source', 'Unknown')} ---\n{doc.page_content}\n\n"
        return context
    except Exception:
        return ""
