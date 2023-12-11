from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    firstname: str = Field(max_length=32)
    lastname: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=6, max_length=50)


class UserIn(BaseModel):
    firstname: str = Field(max_length=32)
    lastname: str = Field(max_length=32)
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=6, max_length=50)
