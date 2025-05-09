from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from starlette import status

from app.database import get_db
from app.domain.expert import expert_crud
from app.domain.expert.expert_schema import ExpertResponse, ExpertRequest, ExpertSearch, ExpertEmbedding

router = APIRouter(
    prefix="/expert",
    tags=["expert"],
)

IMAGE_DIRECTORY = "local_images"


@router.get("/image/{image_number}")
async def get_image(image_number: int):
    # 이미지 번호가 1부터 10 사이인지 확인
    if 1 <= image_number <= 10:
        file_path = Path(IMAGE_DIRECTORY) / f"{image_number}.jpg"  # 예: 1.jpg, 2.jpg, ...

        if file_path.exists() and file_path.is_file():
            # 이미지 파일이 존재하면 반환
            return FileResponse(file_path)
        else:
            return {"error": f"Image {image_number}.jpg not found."}
    else:
        return {"error": "Please enter a number between 1 and 10."}


@router.post("/create/{user_id}", response_model=ExpertResponse)
def create_expert(
        user_id: int,
        req: ExpertRequest,
        db: Session = Depends(get_db),
):
    return expert_crud.create(db, req, user_id)


@router.get("/get/{user_id}", response_model=ExpertResponse)
def get_expert(
        user_id: int,
        db: Session = Depends(get_db),
):
    return expert_crud.get(db, user_id)


@router.delete("/del/{user_id}", status_code=status.HTTP_200_OK)
def delete_expert(
        user_id: int,
        db: Session = Depends(get_db),
):
    return expert_crud.delete(db, user_id)


@router.put("/update/{user_id}", response_model=ExpertResponse)
def update_expert(
        user_id: int,
        req: ExpertRequest,
):
    return expert_crud.update(db, req=req, user_id=user_id)


@router.post("/search/{user_id}", response_model=List[ExpertEmbedding])
def search_expert(
        user_id: str,
        req: ExpertSearch,
        db: Session = Depends(get_db),
):
    """
    - :param user_id: 농장주 id
    - :param req: 지역(다중값), 프로그램 타겟, 프로그램 유형, 시설, 상담방식
    - :return: ai 맞춤 전문가 추천
    """
    return expert_crud.search(db, req, user_id)


@router.post("/main/search", response_model=List[ExpertResponse])
def search_expert(
        db: Session = Depends(get_db),
):
    """
    - :param user_id: 농장주 id
    - :param req: 지역(다중값), 프로그램 타겟, 프로그램 유형, 시설, 상담방식
    - :return: ai 맞춤 전문가 추천
    """
    return expert_crud.main_search(db)


@router.post("/dummydata")
def dummy_data(db: Session = Depends(get_db)):
    expert_crud.dummy_data(db)
