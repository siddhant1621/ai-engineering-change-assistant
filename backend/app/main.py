from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/api/parts/{part_number}", response_model=schemas.PartResponse)
def get_part(
    part_number: str,
    db: Session = Depends(get_db),
):
    part = (
        db.query(models.Part)
        .filter(models.Part.part_number == part_number)
        .first()
    )

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Part not found",
        )

    return part


@app.get(
    "/api/parts/{part_number}/revisions",
    response_model=list[schemas.PartRevisionResponse],
)
def get_part_revisions(
    part_number: str,
    db: Session = Depends(get_db),
):
    part = (
        db.query(models.Part)
        .filter(models.Part.part_number == part_number)
        .first()
    )

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Part not found",
        )

    return (
        db.query(models.PartRevision)
        .filter(models.PartRevision.part_id == part.id)
        .all()
    )


@app.post(
    "/api/parts/{part_number}/revisions",
    response_model=schemas.PartRevisionResponse,
)
@app.delete("/api/revisions/{revision_id}")
def delete_revision(
    revision_id: int,
    db: Session = Depends(get_db),
):
    revision = (
        db.query(models.PartRevision)
        .filter(models.PartRevision.id == revision_id)
        .first()
    )

    if revision is None:
        raise HTTPException(
            status_code=404,
            detail="Revision not found",
        )

    db.delete(revision)
    db.commit()

    return {
        "message": "Revision deleted successfully"
    }
def create_part_revision(
    part_number: str,
    revision: schemas.PartRevisionCreate,
    db: Session = Depends(get_db),
):
    part = (
        db.query(models.Part)
        .filter(models.Part.part_number == part_number)
        .first()
    )

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Part not found",
        )

    db_revision = models.PartRevision(
        part_id=part.id,
        revision=revision.revision,
        lifecycle_state=revision.lifecycle_state,
    )

    db.add(db_revision)
    db.commit()
    db.refresh(db_revision)

    return db_revision