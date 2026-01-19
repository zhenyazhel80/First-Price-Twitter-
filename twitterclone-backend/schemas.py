from pydantic import BaseModel
from datetime import datetime

# --- Input Models (Used for creating data) ---

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TweetCreate(BaseModel):
    content: str


# --- Output Models (Used for returning data) ---

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  
        orm_mode = True        


class Tweet(BaseModel):
    id: int
    content: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
