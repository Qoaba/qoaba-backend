def question_serializer(question) -> dict:
    return {
        "id": str(question["_id"]),
        "topic": question["topic"],
        "question_title": question["question_title"],
        "question": question["question"],
        "solution": question["solution"],
        "difficulty": question["difficulty"],
    }


def questions_serializer(questions) -> list:
    return [question_serializer(question) for question in questions]
