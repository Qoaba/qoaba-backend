
from fastapi import APIRouter, Response, status
from app.models.user_model import User
from app.schemas.user_schema import user_serializer
from app.config.database import user_collection
from app.utils.encryption import encrypt_password, generate_salt, check_password
from app.utils.gravatar import generate_random_avatar_url
from bson import ObjectId

auth_api_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@auth_api_router.post("/login")
async def user_authenticate(user: User, response: Response):
    user_db = user_collection.find_one({"email": user.email})

    if user_db is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"

    if check_password(user.password, user_db["password"], user_db["salt"]):
        user_data = [
            user_db["username"],
            user_db["picture"],
            user_db["role"],
            str(user_db["_id"])
        ]
        return user_data
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"


@auth_api_router.post("/")
async def user_signup(user: User, response: Response):
    password = user.password
    # Check if user already exists
    user_in_db = user_collection.find_one({"email": user.email})
    if user_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "User already exists"

    # Generate avatar url
    user.picture = generate_random_avatar_url(user.email)

    # Set user role
    user.role = "user"

    # Generate salt
    salt = generate_salt()
    hashed_password = encrypt_password(password, salt)
    user.password = hashed_password
    user.salt = salt

    user_collection.insert_one(dict(user))
    return user_collection.find_one({"email": user.email})["email"]

@auth_api_router.put("/{id}")
async def user_update(id: str, user: User, response: Response):
    # Check if a user with the same username already exists
    user_in_db = user_collection.find_one({"username": user.username})
    if user_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "User already exists"

    user_collection.find_one_and_update({"_id": ObjectId(id)}, {
    "$set": {"username": user.username}
    })
    return "Username updated"