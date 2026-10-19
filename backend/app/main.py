from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Engineering Change Assistant API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "AI Engineering Change Assistant backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/api/parts", response_model=list[schemas.PartResponse])
def get_parts(db: Session = Depends(get_db)):
    return db.query(models.Part).all()


@app.post("/api/parts", response_model=schemas.PartResponse)
def create_part(
    part: schemas.PartCreate,
    db: Session = Depends(get_db),
):
    db_part = models.Part(**part.model_dump())

    db.add(db_part)
    db.commit()
    db.refresh(db_part)

    return db_part
