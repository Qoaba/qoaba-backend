from pydantic import BaseModel


class User(BaseModel):
    username: str | None
    email: str
    password: str
    salt: str | None
