
from fastapi import APIRouter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from app.models.user_model import User
from app.schemas.user_schema import user_serializer
from app.config.database import user_collection

from app.utils.encryption import encrypt_password, generate_salt, check_password

auth_api_router = APIRouter()

'''
GET
Pass username and password as GET parameters to authenticate a user. If successful,
returns 200 with username.
'''


@auth_api_router.get("/")
def user_authenticate(user: User):
    user_db = user_serializer(user_collection.find_one({"email": user.email}))

    if user_db is None:
        return Response('Unable to find user', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if check_password(user.password, user_db.password, user_db.salt):
        return Response("Authenticated", status=status.HTTP_200_OK)
    return Response('Wrong username or password', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
POST
Pass username and password as GET parameters to register a new applicant user. If successful,
returns 200 with username.
'''


@auth_api_router.post("/")
def user_signup(user: User):
    password = user.password

    # Generate salt
    salt = generate_salt()
    hashed_password = encrypt_password(password, salt)
    user.password = hashed_password
    user.salt = salt

    _id = user_collection.insert_one(dict(user))
    return user_serializer(user_collection.find({"_id": _id.inserted_id}))
