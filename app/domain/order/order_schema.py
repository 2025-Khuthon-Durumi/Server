from pydantic import BaseModel


class OrderUpdate(BaseModel):
    content: str


class OrderRequest(BaseModel):
    content: str
    expert_id: int


class OrderResponse(BaseModel):
    id: int
    farmer_id: int
    expert_id: int
    content: str
