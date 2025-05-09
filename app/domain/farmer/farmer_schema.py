from pydantic import BaseModel


class FarmerResponse(BaseModel):
    id: int
    name: str
    introduction: str


class FarmerRequest(BaseModel):
    introduction: str
