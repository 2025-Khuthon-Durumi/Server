from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.domain.order.order_schema import OrderRequest, OrderResponse, OrderUpdate
from app.models import Order, User, ExpertProfile


def create_order(db: Session, user_id: int, req: OrderRequest):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    expert = db.query(ExpertProfile).filter(ExpertProfile.id == req.expert_id).first()
    if not expert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Expert not found')
    new_order = Order(
        farmer_id=user_id,
        expert_id=req.expert_id,
        content=req.content
    )
    db.add(new_order)
    db.commit()
    return new_order


def get_farmer_orders(db: Session, user_id: int):
    farmer = db.query(User).filter(User.id == user_id).first()
    if not farmer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="farmer not found")
    orders = db.query(Order).filter(Order.farmer_id == user_id).all()
    return orders


def get_expert_orders(db: Session, user_id: int):
    expert = db.query(User).filter(User.id == user_id).first()
    if not expert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="expert not found")
    orders = db.query(Order).filter(Order.farmer_id == user_id).all()
    return orders


def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    return order


def update_order(db: Session, order_id: int, req: OrderUpdate):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    order.content = req.content
    db.commit()
    return order


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    db.delete(order)
    db.commit()
