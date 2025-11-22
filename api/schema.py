from pydantic import BaseModel, EmailStr, Field
# from typing import Optional


class UserRegisterRequest(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=6, example="StrongPass123")
    confirm_password: str = Field(..., min_length=6, example="StrongPass123")

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="StrongPass123")

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr