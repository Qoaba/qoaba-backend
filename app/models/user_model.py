from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    picture: str | None = None
    role: str | None = None
    password: str
    salt: str | None = None
