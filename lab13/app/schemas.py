from pydantic import BaseModel
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    profile: Optional['Profile'] = None

    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    full_name: str
    email: str

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
