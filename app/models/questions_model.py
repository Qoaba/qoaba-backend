from pydantic import BaseModel


class Question(BaseModel):
    topic: str
    question_title: str
    question: str
    solution: str
    difficulty: str
