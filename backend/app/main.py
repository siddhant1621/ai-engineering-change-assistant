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


# ---------------------------------------------------------
# ROOT / HEALTH
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# PARTS
# ---------------------------------------------------------

@app.get(
    "/api/parts",
    response_model=list[schemas.PartResponse],
)
def get_parts(
    db: Session = Depends(get_db),
):
    return db.query(models.Part).all()


@app.post(
    "/api/parts",
    response_model=schemas.PartResponse,
)
def create_part(
    part: schemas.PartCreate,
    db: Session = Depends(get_db),
):
    db_part = models.Part(**part.model_dump())

    db.add(db_part)
    db.commit()
    db.refresh(db_part)

    return db_part


@app.get(
    "/api/parts/{part_number}",
    response_model=schemas.PartResponse,
)
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


# ---------------------------------------------------------
# PART REVISIONS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# BOM
# ---------------------------------------------------------

@app.get(
    "/api/parts/{part_number}/bom",
    response_model=list[schemas.BomItemResponse],
)
def get_bom(
    part_number: str,
    db: Session = Depends(get_db),
):
    parent = (
        db.query(models.Part)
        .filter(models.Part.part_number == part_number)
        .first()
    )

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent part not found",
        )

    bom_items = (
        db.query(models.BomItem)
        .filter(models.BomItem.parent_part_id == parent.id)
        .all()
    )

    return [
        {
            "id": item.id,
            "parent_part_number": parent.part_number,
            "child_part_number": item.child_part.part_number,
            "child_name": item.child_part.name,
            "quantity": item.quantity,
        }
        for item in bom_items
    ]


@app.post(
    "/api/parts/{part_number}/bom",
    response_model=schemas.BomItemResponse,
)
def add_bom_item(
    part_number: str,
    bom_item: schemas.BomItemCreate,
    db: Session = Depends(get_db),
):
    parent = (
        db.query(models.Part)
        .filter(models.Part.part_number == part_number)
        .first()
    )

    if parent is None:
        raise HTTPException(
            status_code=404,
            detail="Parent part not found",
        )

    child = (
        db.query(models.Part)
        .filter(
            models.Part.part_number == bom_item.child_part_number
        )
        .first()
    )

    if child is None:
        raise HTTPException(
            status_code=404,
            detail="Child part not found",
        )

    if parent.id == child.id:
        raise HTTPException(
            status_code=400,
            detail="A part cannot contain itself",
        )

    db_bom_item = models.BomItem(
        parent_part_id=parent.id,
        child_part_id=child.id,
        quantity=bom_item.quantity,
    )

    db.add(db_bom_item)
    db.commit()
    db.refresh(db_bom_item)

    return {
        "id": db_bom_item.id,
        "parent_part_number": parent.part_number,
        "child_part_number": child.part_number,
        "child_name": child.name,
        "quantity": db_bom_item.quantity,
    }
@app.get("/api/parts/{part_number}/where-used")
def get_where_used(
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

    usages = (
        db.query(models.BomItem)
        .filter(models.BomItem.child_part_id == part.id)
        .all()
    )

    return [
        {
            "bom_item_id": item.id,
            "parent_part_number": item.parent_part.part_number,
            "parent_name": item.parent_part.name,
            "quantity": item.quantity,
        }
        for item in usages
    ]

@app.delete("/api/bom-items/{bom_item_id}")
def delete_bom_item(
    bom_item_id: int,
    db: Session = Depends(get_db),
):
    bom_item = (
        db.query(models.BomItem)
        .filter(models.BomItem.id == bom_item_id)
        .first()
    )

    if bom_item is None:
        raise HTTPException(
            status_code=404,
            detail="BOM item not found",
        )

    db.delete(bom_item)
    db.commit()

    return {
        "message": "BOM item deleted successfully"
    }