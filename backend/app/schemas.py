from pydantic import BaseModel

class EngineeringChangeCreate(BaseModel):
    change_number: str
    title: str
    description: str
    reason: str
    status: str = "Draft"
    owner: str
    affected_part_number: str


class EngineeringChangeResponse(BaseModel):
    id: int
    change_number: str
    title: str
    description: str
    reason: str
    status: str
    owner: str
    affected_part_number: str
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


class BomItemCreate(BaseModel):
    child_part_number: str
    quantity: float = 1


class BomItemResponse(BaseModel):
    id: int
    parent_part_number: str
    child_part_number: str
    child_name: str
    quantity: float