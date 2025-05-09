from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from starlette import status

from app.database import get_db
from app.domain.farmer import farmer_crud
from app.domain.farmer.farmer_schema import FarmerResponse, FarmerRequest

router = APIRouter(
    prefix="/farmer",
    tags=["farmer"],
)


@router.post("/create/{user_id}", response_model=FarmerResponse)
def farmer_create(user_id: int, req: FarmerRequest, db: Session = Depends(get_db)):
    return farmer_crud.create(db, user_id, req)
