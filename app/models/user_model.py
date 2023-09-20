from pydantic import BaseModel


class User(BaseModel):
    email_verified: bool | None = None
    picture: str | None = None
    locale: str | None = None
    role: str | None = None
