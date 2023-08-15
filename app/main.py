from fastapi import FastAPI
from app.routes.questions_route import question_api_router

app = FastAPI()

app.include_router(question_api_router)