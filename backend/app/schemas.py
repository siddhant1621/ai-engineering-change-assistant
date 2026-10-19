from pydantic import BaseModel


class PartBase(BaseModel):
    part_number: str
    name: str
    revision: str
    lifecycle_state: str


class PartCreate(PartBase):
    pass


class PartResponse(PartBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class PartRevisionCreate(BaseModel):
    revision: str
    lifecycle_state: str


class PartRevisionResponse(BaseModel):
    id: int
    part_id: int
    revision: str
    lifecycle_state: str

    model_config = {
        "from_attributes": True
    }