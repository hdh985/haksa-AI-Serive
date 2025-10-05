from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def build_vector_db():
    print("📄 PDF 로드 중...")
    loader = PyPDFLoader("data/guide.pdf")
    documents = loader.load()

    print("✂️ 텍스트 분리 중...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    print("🧠 임베딩 생성 중...")
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")

    print("💾 벡터DB 저장 중...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="./db/chroma_db"
    )
    vectordb.persist()
    print("✅ 학습 완료! DB 생성됨: ./db/chroma_db")

if __name__ == "__main__":
    build_vector_db()
