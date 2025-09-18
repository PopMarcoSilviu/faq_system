from fastapi import APIRouter
from text_completion.text_completer import TextCompleter
from vector_db.pg_vector_db import PGVectorDB
from qa_system.qa_system import QASystem
from models.qa_system_models import QuestionRequest, QuestionResponse
from fastapi.responses import JSONResponse
import os
from typing import Literal


router = APIRouter(prefix="", tags=["qa"])


vector_db = PGVectorDB('qa_collection')
llm = TextCompleter()
qa_system = QASystem(vector_db, llm)



@router.post("/ask-question")
async def ask_question(request: QuestionRequest) -> QuestionResponse:
    qa_system_response = qa_system.answer(request.user_question)
    response = QuestionResponse(**qa_system_response)
    return response



@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})
  


