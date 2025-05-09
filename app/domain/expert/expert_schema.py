from typing import List

from pydantic import BaseModel


class ExpertRequest(BaseModel):
    image: int
    job: str
    career: str
    region: str
    title: str
    price: int
    introduction: str


class ExpertResponse(BaseModel):
    id: int
    image: str
    job: str
    career: str
    region: str

    title: str
    price: int
    introduction: str

    name: str
    phone: str


class ExpertEmbedding(BaseModel):
    id: int
    job: str
    career: str
    image: str
    title: str
    price: int
    introduction: str
    region: str
    name: str
    similarity: float


class ExpertSearch(BaseModel):
    region: str
    target: str
    category: str
    facilities: str
    offline: str

