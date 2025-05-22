from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Input Models (Used for creating data) ---

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TweetCreate(BaseModel):
    content: str
    likes: Optional[int] = 0  # Optional likes when creating


# --- Output Models (Used for returning data) ---

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True

class Tweet(BaseModel):
    id: int
    content: str
    owner_id: int
    likes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Optional: Like output model (if needed in the future) ---

class Like(BaseModel):
    id: int
    user_id: int
    tweet_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
