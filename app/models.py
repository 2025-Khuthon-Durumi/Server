from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped, declarative_base
from app.domain.user.user_schema import Role

# Base를 declarative_base()로 정의
Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    farmer_profiles: Mapped[list['FarmerProfile']] = relationship("FarmerProfile", back_populates="user")
    expert_profiles: Mapped[list['ExpertProfile']] = relationship("ExpertProfile", back_populates="user")


class FarmerProfile(Base):
    __tablename__ = 'FarmerProfile'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'), primary_key=True)
    introduction: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped['User'] = relationship("User", back_populates="farmer_profiles")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="farmer")


class ExpertProfile(Base):
    __tablename__ = 'ExpertProfile'

    id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'), primary_key=True)
    image: Mapped[int] = mapped_column(Integer, nullable=True)
    career: Mapped[str] = mapped_column(String, nullable=True)

    job: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    # do: Mapped[str] = mapped_column(String, nullable=True)  # 도
    # si: Mapped[str] = mapped_column(String, nullable=True)  # 시
    # gu: Mapped[str] = mapped_column(String, nullable=True)  # 구
    # dong: Mapped[str] = mapped_column(String, nullable=True)  # 동/읍/면

    title: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=True)
    introduction: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped['User'] = relationship("User", back_populates="expert_profiles")
    orders: Mapped[list['Order']] = relationship("Order", back_populates="expert")


class Order(Base):
    __tablename__ = 'Order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey('FarmerProfile.id'))
    expert_id: Mapped[int] = mapped_column(Integer, ForeignKey('ExpertProfile.id'))
    content: Mapped[str] = mapped_column(String, nullable=True)

    farmer: Mapped['FarmerProfile'] = relationship("FarmerProfile", back_populates="orders")
    expert: Mapped['ExpertProfile'] = relationship("ExpertProfile", back_populates="orders")
    # reviews = relationship("Review", back_populates="order")


# class Review(Base):
#     __tablename__ = 'review'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     order_id: Mapped[int] = mapped_column(Integer, ForeignKey('order.id'))
#     rating: Mapped[int] = mapped_column(Integer, nullable=True)
#     comment: Mapped[str] = mapped_column(String, nullable=True)
#
#     order: Mapped['Order'] = relationship("Order", back_populates="reviews")
#     service: Mapped['Service'] = relationship("Service", back_populates="reviews")


# from sqlalchemy import Integer, String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
#
# # 도 (Province) 테이블
# class Province(Base):
#     __tablename__ = 'Province'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)  # 예: 서울특별시
#
#     # Province와 관련된 City (시)들의 관계
#     cities: Mapped[list['City']] = relationship("City", back_populates="province")

#
# # 시 (City) 테이블
# class City(Base):
#     __tablename__ = 'City'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)  # 예: 서울시
#     province_id: Mapped[int] = mapped_column(Integer, ForeignKey('Province.id'))
#
#     # City와 관련된 District (구)들의 관계
#     district: Mapped[list['District']] = relationship("District", back_populates="city")
#     province: Mapped['Province'] = relationship("Province", back_populates="cities")
#
#
# # 구 (District) 테이블
# class District(Base):
#     __tablename__ = 'District'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)  # 예: 강남구
#     city_id: Mapped[int] = mapped_column(Integer, ForeignKey('City.id'))
#
#     # District와 관련된 Neighborhood (동/읍/면)들의 관계
#     neighborhood: Mapped[list['Neighborhood']] = relationship("Neighborhood", back_populates="district")
#     city: Mapped['City'] = relationship("City", back_populates="district")
#
#
# # 동/읍/면 (Neighborhood) 테이블
# class Neighborhood(Base):
#     __tablename__ = 'Neighborhood'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)  # 예: 삼성동
#     district_id: Mapped[int] = mapped_column(Integer, ForeignKey('District.id'))
#
#     district: Mapped['District'] = relationship("District", back_populates="neighborhood")
#
#
# # 주소 (Address) 테이블
# class Address(Base):
#     __tablename__ = 'Address'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     expert_profile_id:
