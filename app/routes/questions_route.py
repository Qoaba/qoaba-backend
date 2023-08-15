from fastapi import APIRouter

from app.models.questions_model import Question
from app.config.database import collection_name

from app.schemas.questions_schema import questions_serializer, question_serializer
from bson import ObjectId

question_api_router = APIRouter()

# retrieve
@question_api_router.get("/")
async def get_questions():
    questions = questions_serializer(collection_name.find())
    return questions

@question_api_router.get("/{id}")
async def get_question(id: str):
    return questions_serializer(collection_name.find_one({"_id": ObjectId(id)}))


# post
@question_api_router.post("/")
async def create_question(question: Question):
    _id = collection_name.insert_one(dict(question))
    return questions_serializer(collection_name.find({"_id": _id.inserted_id}))


# update
@question_api_router.put("/{id}")
async def update_question(id: str, question: Question):
    collection_name.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": dict(question)
    })
    return questions_serializer(collection_name.find({"_id": ObjectId(id)}))

# delete
@question_api_router.delete("/{id}")
async def delete_question(id: str):
    collection_name.find_one_and_delete({"_id": ObjectId(id)})
    return {"status": "ok"}