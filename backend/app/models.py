from sqlalchemy import Column, ForeignKey, Integer, String
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