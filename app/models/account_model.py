from pydantic import BaseModel


class Account(BaseModel):
    name: str | None = None
    email: str
    password: str
    type: str | None = None
    salt: str | None = None
    userId: str | None = None
