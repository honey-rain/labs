from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/{user_id}/profile", response_model=schemas.Profile)
def create_profile(user_id: int, profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile, user_id=user_id)

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, user_id=user_id)

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, post_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, post_id=post_id, user_id=user_id)
