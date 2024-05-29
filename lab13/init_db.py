from app.database import SessionLocal, engine
from app import models

def init_db():
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    db.close()

if __name__ == "__main__":
    init_db()
