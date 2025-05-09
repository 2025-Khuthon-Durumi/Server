from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.domain.farmer.farmer_schema import FarmerResponse, FarmerRequest
from app.models import FarmerProfile, User


def create(db: Session, user_id: int, req: FarmerRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    farmer = FarmerProfile(id=user_id, introduction=req.introduction)
    db.add(farmer)
    db.commit()
    return FarmerResponse(
        id=farmer.id,
        introduction=farmer.introduction,
        name=user.name
    )


def get_farmer(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    farmer = db.query(FarmerProfile).filter(FarmerProfile.id == user_id).first()
    if farmer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return FarmerResponse(
        id=farmer.id,
        name=user.name
    )

