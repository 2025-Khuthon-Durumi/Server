from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.testing import db
from starlette import status

from app.database import get_db
from app.domain.order import order_crud
from app.domain.order.order_schema import OrderRequest, OrderResponse, OrderUpdate

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.post("/create/{user_id}", response_model=OrderResponse)
def create_order(user_id: int, req: OrderRequest , db: Session = Depends(get_db)):
    """
    :param user_id: 농장주(신청자의 user_id)
    :param req: content: 신청 글 작성
    """
    return order_crud.create_order(db, user_id, req)


@router.get("/list/{farmer_id}", response_model=OrderResponse)
def get_farmer_orders(farmer_id: int, db: Session = Depends(get_db)):
    """
    #### 전문가 입장에서 신청 들어온거 전체보기
    """
    return order_crud.get_farmer_orders(db, farmer_id)


@router.get("/list/{expert_id}", response_model=OrderResponse)
def get_expert_orders(expert_id: int, db: Session = Depends(get_db)):
    """
    #### 전문가 입장에서 신청 들어온거 전체보기
    """
    return order_crud.get_expert_orders(db, expert_id)


@router.get("/get/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    order 하나 반환
    """
    return order_crud.get_order(db, order_id)


@router.delete("/del/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_crud.delete_order(db, order_id)


@router.put("/update/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, req: OrderUpdate, db: Session = Depends(get_db)):
    return order_crud.update_order(db, order_id, req)
