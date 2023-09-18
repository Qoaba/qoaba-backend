
from fastapi import APIRouter, Response, status
from app.models.account_model import Account
from app.schemas.user_schema import user_serializer
from app.config.database import account_collection
from app.utils.encryption import encrypt_password, generate_salt, check_password
from app.utils.gravatar import generate_random_avatar_url
from bson import ObjectId

auth_api_router = APIRouter(
    prefix="/api/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


@auth_api_router.post("/login")
async def user_authenticate(user: Account, response: Response):
    user_db = account_collection.find_one({"email": user.email})

    if user_db is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"

    if check_password(user.password, user_db["password"], user_db["salt"]):
        user_data = [
            user_db["username"],
            user_db["picture"],
            user_db["role"],
            str(user_db["_id"]),
        ]
        return user_data
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"


@auth_api_router.post("/")
async def user_signup(account: Account, response: Response):
    password = account.password
    # Check if user already exists
    account_in_db = account_collection.find_one({"email": account.email})
    if account_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "User already exists"

    # Generate avatar url
    account.picture = generate_random_avatar_url(account.email)

    # Set user role
    account.role = "user"

    # Generate salt
    salt = generate_salt()
    hashed_password = encrypt_password(password, salt)
    account.password = hashed_password
    account.salt = salt

    account_collection.insert_one(dict(account))
    return account_collection.find_one({"email": account.email})["email"]


@auth_api_router.put("/{id}/username")
async def username_update(id: str, account: Account, response: Response):
    account_in_db = account_collection.find_one({"username": account.username})
    if account_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "User already exists"

    account_collection.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {"username": account.username}
    })
    return "Username updated"


@auth_api_router.put("/{id}/email")
async def email_update(id: str, account: Account, response: Response):
    email_in_db = account_collection.find_one({"email": account.email})
    if email_in_db is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return "Email already exists"

    account_db = account_collection.find_one({"_id": ObjectId(id)})
    if check_password(account.password, account_db["password"], account_db["salt"]):
        account_collection.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {"email": account.email}
        })
        return "Email updated"
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"


@auth_api_router.put("/{id}/password")
async def password_update(id: str, account: Account, response: Response):
    current_password = account.password.split(" ")[0]
    new_password = account.password.split(" ")[1]

    account_db = account_collection.find_one({"_id": ObjectId(id)})
    if check_password(current_password, account_db["password"], account_db["salt"]):
        salt = generate_salt()
        hashed_password = encrypt_password(new_password, salt)

        account_collection.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": {"password": hashed_password, "salt": salt}
        })
        return "Password updated"
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"


@auth_api_router.delete("/{id}")
async def user_delete(id: str, account: Account, response: Response):
    account_db = account_collection.find_one({"_id": ObjectId(id)})
    if check_password(account.password, account_db["password"], account_db["salt"]) and account_db["email"] == account.email:
        account_collection.find_one_and_delete({"_id": ObjectId(id)})
        return "User deleted"
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "User not authenticated"
