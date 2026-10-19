from sqlalchemy import Column, Integer, String

from .database import Base


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    revision = Column(String, nullable=False)
    lifecycle_state = Column(String, nullable=False)