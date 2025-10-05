import os
from dotenv import load_dotenv

# ✅ LangChain 0.2+ 버전용 import
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def build_vector_db():
    print("📄 PDF 로드 중...")

    # ✅ 경로를 절대경로 기반으로 안전하게 처리
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "data", "Haksa.pdf")
    db_dir = os.path.join(base_dir, "db", "chroma_db")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF 파일을 찾을 수 없습니다: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
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
        persist_directory=db_dir
    )
    vectordb.persist()

    print(f"✅ 학습 완료! DB 생성됨: {db_dir}")

if __name__ == "__main__":
    build_vector_db()
