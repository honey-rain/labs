from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Post(BaseModel):
    id: int
    title: str
    content: str

posts_db: Dict[int, Post] = {
    1: Post(id=1, title="First Post", content="This is the first post"),
    2: Post(id=2, title="Second Post", content="This is the second post")
}

@router.get("/posts")
def get_posts():
    return list(posts_db.values())

@router.post("/posts")
def create_post(post: Post):
    if post.id in posts_db:
        raise HTTPException(status_code=400, detail="Post ID already exists")
    posts_db[post.id] = post
    return post

@router.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    posts_db[post_id] = post
    return post

@router.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    del posts_db[post_id]
    return {"detail": "Post deleted"}
