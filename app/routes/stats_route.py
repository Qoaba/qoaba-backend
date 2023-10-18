from fastapi import APIRouter
from app.config.database import stats_collection
from bson import ObjectId

stats_api_router = APIRouter(
    prefix="/api/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)


@stats_api_router.post("/attempt")
async def record_attempted(data: dict):
    existing_document = stats_collection.find_one(
        {"_id": ObjectId(data["userId"])})

    if existing_document:
        stats_collection.update_one(
            {"_id": ObjectId(data["userId"])},
            {
                "$push": {
                    "attemptedQuestions": {
                        "isCorrect": data["isCorrect"],
                        "questionId": ObjectId(data["questionId"]),
                        "timeStamp": data["timeStamp"]
                    }
                }
            }
        )
    else:
        stats_collection.insert_one({
            "_id": ObjectId(data["userId"]),
            "attemptedQuestions": [
                {
                    "isCorrect": data["isCorrect"],
                    "questionId": ObjectId(data["questionId"]),
                    "timeStamp": data["timeStamp"]
                }
            ]
        })

    return {"message": "success"}
