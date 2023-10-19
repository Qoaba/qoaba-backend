from fastapi import APIRouter
from app.config.database import stats_collection
from bson import ObjectId
from app.routes.questions_route import get_question, get_questions

stats_api_router = APIRouter(
    prefix="/api/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)


@stats_api_router.post("/")
async def record_attempted(data: dict):
    userId = ObjectId(data["userId"])
    questionId = ObjectId(data["questionId"])

    existing_document = stats_collection.find_one({"_id": userId})

    if existing_document:
        existing_entry = next(
            (
                entry
                for entry in existing_document["attempted_questions"]
                if entry["questionId"] == questionId
            ),
            None,
        )

        if existing_entry:
            stats_collection.update_one(
                {"_id": userId, "attempted_questions.questionId": questionId},
                {
                    "$set": {
                        "attempted_questions.$.timestamp": data["timestamp"],
                        "attempted_questions.$.is_correct": data["isCorrect"],
                    }
                },
            )
        else:
            stats_collection.update_one(
                {"_id": userId},
                {
                    "$push": {
                        "attempted_questions": {
                            "is_correct": data["isCorrect"],
                            "questionId": questionId,
                            "timestamp": data["timestamp"],
                        }
                    }
                },
            )
    else:
        stats_collection.insert_one(
            {
                "_id": userId,
                "attempted_questions": [
                    {
                        "is_correct": data["isCorrect"],
                        "questionId": questionId,
                        "timestamp": data["timestamp"],
                    }
                ],
            }
        )

    return {"message": "success"}


@stats_api_router.get("/{id}/attempts")
async def get_stats(id: str):
    existing_document = stats_collection.find_one({"_id": ObjectId(id)})
    all_questions = await get_questions()

    solved_problems = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
    total_problems = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}

    if existing_document:
        attempted_questions = existing_document["attempted_questions"]
        for question in attempted_questions:
            questionId = str(question["questionId"])
            question_data = await get_question(questionId)
            if question["is_correct"]:
                solved_problems[question_data["data"][0]["difficulty"]] += 1

    for question in all_questions:
        total_problems[question["difficulty"]] += 1

    result = {"solved": solved_problems, "total": total_problems}
    return result
