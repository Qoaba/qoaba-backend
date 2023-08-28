from pydantic import BaseModel


class User(BaseModel):
    username: str | None = None
    email: str
    picture: str | None = None
    password: str
    salt: str | None = None
