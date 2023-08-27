
from fastapi import APIRouter, Response, status
from app.models.user_model import User
from app.schemas.user_schema import user_serializer
from app.config.database import user_collection
from app.utils.encryption import encrypt_password, generate_salt, check_password

auth_api_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

'''
GET
Pass username and password as GET parameters to authenticate a user. If successful,
returns 200 with username.
'''


@auth_api_router.post("/login")
def user_authenticate(user: User, response: Response):
    user_db = user_collection.find_one({"email": user.email})

    if user_db is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"
    
    if check_password(user.password, user_db["password"], user_db["salt"]):
        return user_db["username"]
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"

'''
POST
Pass username and password as GET parameters to register a new applicant user. If successful,
returns 200 with username.
'''

@auth_api_router.post("/")
def user_signup(user: User, response: Response):
    password = user.password
    # Check if user already exists
    user_in_db = user_collection.find_one({"email": user.email})
    if user_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "User already exists"
    
    # Generate salt
    salt = generate_salt()
    hashed_password = encrypt_password(password, salt)
    user.password = hashed_password
    user.salt = salt

    user_collection.insert_one(dict(user))
    return user_collection.find_one({"email": user.email})["email"]
