from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import load_rag_pipeline

app = FastAPI(title="Kyung Hee Haksa Chatbot")

qa = load_rag_pipeline()

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask_question(question: Question):
    result = qa.invoke({"query": question.query})
    return {"answer": result["result"]}
