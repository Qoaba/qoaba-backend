from pydantic import BaseModel


class Account(BaseModel):
    username: str | None = None
    email: str
    picture: str | None = None
    role: str | None = None
    password: str
    salt: str | None = None
