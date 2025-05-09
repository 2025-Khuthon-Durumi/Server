from sqlalchemy.orm import Session

from app.domain.farmer import farmer_crud
from app.domain.user.user_schema import UserRequest, Role
from app.models import User


def create(db: Session, req: UserRequest):
    new_user = User(name=req.name,
                    role=req.role,
                    phone=req.phone,
                    )
    db.add(new_user)
    db.commit()

    # if new_user.role == Role.FARMER:
    #     farmer_crud.create(db, new_user.id)
    return new_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update(db: Session, user_id: int, req: UserRequest):
    user = db.query(User).filter(User.id == user_id).first()
    user.name = req.name
    user.role = req.role
    user.phone = req.phone
    db.commit()
    return user


def delete(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return "ok"