from fastapi import FastAPI
from routers.qa_routers import router as qa_router

app = FastAPI(title="FAQ System")
app.include_router(qa_router)
