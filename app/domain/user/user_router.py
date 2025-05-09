from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.domain.user import user_crud
from app.domain.user.user_schema import UserResponse, UserRequest
from app.models import User

# 라우터 함수에서는 데이터를 조회하는 부분을 포함해도 되지만
# 파이보 프로젝트는 데이터를 처리하는 부분을 question_crud.py 파일에 분리하여 작성한다

# 매핑하는 부분 (controller 느낌 ?)
router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/create", response_model=UserResponse)
def create(req: UserRequest, db: Session = Depends(get_db)):
    return user_crud.create(db, req)


@router.get("/get/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_user(db, user_id)


@router.put("/update/{user_id}", response_model=UserResponse)
def update(user_id: int, req: UserRequest, db: Session = Depends(get_db)):
    return user_crud.update(db, user_id, req)


@router.delete("/del/{user_id}", status_code=status.HTTP_200_OK)
def delete(user_id: int, db: Session = Depends(get_db)):
    user_crud.delete(db, user_id)
