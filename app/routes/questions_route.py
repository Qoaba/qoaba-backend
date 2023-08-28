from fastapi import APIRouter

from app.models.questions_model import Question
from app.config.database import question_collection

from app.schemas.questions_schema import questions_serializer, question_serializer
from bson import ObjectId

question_api_router = APIRouter(
    prefix="/api/questions",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# retrieve

@question_api_router.get("/")
async def get_questions():
    questions = questions_serializer(question_collection.find())
    return questions


@question_api_router.get("/{id}")
async def get_question(id: str):
    question = questions_serializer(question_collection.find({"_id": ObjectId(id)}))
    return {"status": "ok", "data": question}


# post
@question_api_router.post("/")
async def create_question(question: Question):
    _id = question_collection.insert_one(dict(question))
    return questions_serializer(question_collection.find({"_id": _id.inserted_id}))


# update
@question_api_router.put("/{id}")
async def update_question(id: str, question: Question):
    question_collection.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(question)
    })
    return questions_serializer(question_collection.find({"_id": ObjectId(id)}))

# delete


@question_api_router.delete("/{id}")
async def delete_question(id: str):
    question_collection.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok"}
