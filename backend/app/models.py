from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    lifecycle_state = Column(String, nullable=False)

    revisions = relationship(
        "PartRevision",
        back_populates="part",
        cascade="all, delete-orphan",
    )


class PartRevision(Base):
    __tablename__ = "part_revisions"

    id = Column(Integer, primary_key=True, index=True)

    part_id = Column(
        Integer,
        ForeignKey("parts.id"),
        nullable=False,
    )

    revision = Column(String, nullable=False)
    lifecycle_state = Column(String, nullable=False)

    part = relationship(
        "Part",
        back_populates="revisions",
    )


class BomItem(Base):
    __tablename__ = "bom_items"

    id = Column(Integer, primary_key=True, index=True)

    parent_part_id = Column(
        Integer,
        ForeignKey("parts.id"),
        nullable=False,
    )

    child_part_id = Column(
        Integer,
        ForeignKey("parts.id"),
        nullable=False,
    )

    quantity = Column(Float, nullable=False, default=1)

    parent_part = relationship(
        "Part",
        foreign_keys=[parent_part_id],
    )

    child_part = relationship(
        "Part",
        foreign_keys=[child_part_id],
    )