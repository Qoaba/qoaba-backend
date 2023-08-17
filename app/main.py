from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.questions_route import question_api_router

app = FastAPI()

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL here
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(question_api_router)
