from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    favorites: List["FavoriteEventOut"] = []

    class Config:
        orm_mode = True


class FavoriteEventCreate(BaseModel):
    event_id: str
    name: str
    url: str
    date: datetime
    image_url: Optional[str] = None


class FavoriteEventOut(FavoriteEventCreate):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



