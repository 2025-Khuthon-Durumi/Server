import base64
import string

import numpy as np
import random

from fastapi import HTTPException
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from starlette import status

from app.domain.expert.expert_schema import ExpertRequest, ExpertResponse, ExpertSearch, ExpertEmbedding
from app.domain.user import user_crud
from app.domain.user.user_schema import Role
from app.models import ExpertProfile, User, FarmerProfile


def image_to_base64(image_path: str) -> str:
    """이미지 파일을 Base64로 변환"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def create(db: Session, req: ExpertRequest, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    new_expert = ExpertProfile(
        id=user_id,
        image=req.image,
        job=req.job,
        career=req.career,
        region=req.region,
        title=req.title,
        price=req.price,
        introduction=req.introduction,
    )
    db.add(new_expert)
    db.commit()

    return ExpertResponse(
        id=new_expert.id,
        image=f"/local_images/{new_expert.image % 10 + 1}.jpg",
        job=new_expert.job,
        career=new_expert.career,
        region=new_expert.region,
        title=new_expert.title,
        price=new_expert.price,
        introduction=new_expert.introduction,
        name=user.name,
        phone=user.phone
    )


def get(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    expert = db.query(ExpertProfile).filter(ExpertProfile.id == user_id).first()
    if expert is None:
        raise HTTPException(status_code=404, detail='Expert not found')

    return ExpertResponse(
        id=expert.id,
        image=f"/local_images/{expert.image % 10 + 1}.jpg",
        job=expert.job,
        career=expert.career,
        region=expert.region,
        title=expert.title,
        price=expert.price,
        introduction=expert.introduction,
        name=user.name,
        phone=user.phone
    )


def delete(db: Session, user_id: int):
    expert = db.query(ExpertProfile).filter(ExpertProfile.id == user_id).first()
    if expert is None:
        raise HTTPException(status_code=404, detail='Expert not found')
    db.delete(expert)
    db.commit()
    return "ok"


def update(db: Session, req: ExpertRequest, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    expert = db.query(ExpertProfile).filter(ExpertProfile.id == user_id).first()
    if expert is None:
        raise HTTPException(status_code=404, detail='Expert not found')
    expert.image = req.image
    expert.job = req.job
    expert.career = req.career
    expert.do = req.do
    expert.si = req.si
    expert.gu = req.gu
    expert.dong = req.dong

    db.commit()
    return ExpertResponse(
        id=expert.id,
        image=f"/local_images/{expert.image % 10 + 1}.jpg",
        job=expert.job,
        career=expert.career,
        region=expert.region,
        title=expert.title,
        price=expert.price,
        introduction=expert.introduction,
        name=user.name,
        phone=user.phone
    )

expert_data = {
    "유아": {
        "정신기능 예방": ["놀이치료사", "유아트숍교사", "아동상담사"],
        "정신기능 치료재활": ["언어재활사", "아동심리상담사", "행동치료사"],
        "신체기능 예방": ["유아체육강사", "아동발달지도사"],
        "신체기능 치료재활": ["작업치료사", "물리치료사"]
    },
    "청소년": {
        "정신기능 예방": ["진로상담사", "정신건강상담사", "사회복지사"],
        "정신기능 치료재활": ["임상심리사", "정신건강상담사", "정신과 간호사"],
        "신체기능 예방": ["운동처방사", "생활체육지도사"],
        "신체기능 치료재활": ["작업치료사", "재활트레이너"]
    },
    "성인": {
        "정신기능 예방": ["심리상담사", "스트레스코칭지도사", "명상지도사"],
        "정신기능 치료재활": ["임상심리사", "정신건강사회복지사", "인지행동치료사"],
        "신체기능 예방": ["건강운동관리사", "웰니스코치"],
        "신체기능 치료재활": ["물리치료사", "운동처방사"]
    },
    "노인": {
        "정신기능 예방": ["노인심리상담사", "회상치료사", "정신지원사"],
        "정신기능 치료재활": ["치매전문상담사", "임상심리사", "정신건강사회복지사"],
        "신체기능 예방": ["실버체육지도사", "원예치료사", "음악치료사"],
        "신체기능 치료재활": ["작업치료사", "물리치료사", "간호사"]
    }
}

model = SentenceTransformer('all-MiniLM-L6-v2')


# def extract_keywords(texts):
#     """전문가 소개에서 중요한 키워드를 추출"""
#     vectorizer = TfidfVectorizer(stop_words='english')
#     X = vectorizer.fit_transform(texts)
#     feature_names = np.array(vectorizer.get_feature_names_out())
#
#     # 상위 5개 키워드 추출
#     top_keywords = []
#     for i in range(len(texts)):
#         sorted_idx = np.argsort(X[i].toarray()).flatten()[::-1][:5]
#         top_keywords.append(list(feature_names[sorted_idx]))
#     return top_keywords
#
#
# def get_farmer_keywords(farmer_introduction):
#     """농부의 요구사항에서 주요 키워드 추출"""
#     vectorizer = TfidfVectorizer(stop_words='english')
#     farmer_vector = vectorizer.fit_transform([farmer_introduction])
#     feature_names = np.array(vectorizer.get_feature_names_out())
#
#     # 상위 5개 키워드 추출
#     sorted_idx = np.argsort(farmer_vector.toarray()).flatten()[::-1][:5]
#     farmer_keywords = list(feature_names[sorted_idx])
#     return farmer_keywords


def filtering(req: ExpertSearch, db: Session):
    jobs = expert_data[req.target][req.category]
    experts = db.query(ExpertProfile).all()

    expert_list = []
    for expert in experts:
        if expert.region in req.region and expert.job in jobs:
            expert_list.append(expert)
    return expert_list


# cosine 함수가 numpy 배열이나 리스트를 처리할 수 있도록 수정
def calculate_similarity(expert_embedding, farmer_embedding):
    # expert_embedding과 farmer_embedding이 numpy 배열로 되어 있는지 확인
    if isinstance(expert_embedding, np.ndarray) and isinstance(farmer_embedding, np.ndarray):
        # numpy 배열로 변환하여 유사도 계산
        return 1 - cosine(expert_embedding, farmer_embedding)
    else:
        raise ValueError("Embeddings should be numpy arrays.")


def compare_keywords(expert_keywords, farmer_keywords):
    """전문가의 키워드와 농부의 키워드를 비교하여 유사도 계산"""
    common_keywords = set(expert_keywords) & set(farmer_keywords)
    similarity_score = len(common_keywords) / max(len(expert_keywords), len(farmer_keywords))
    return similarity_score


def search(db: Session, req: ExpertSearch, user_id):
    filtered_experts = filtering(req, db)
    farmer = db.query(FarmerProfile).filter(FarmerProfile.id == user_id).first()

    expert_embeddings = [model.encode(expert.introduction) for expert in filtered_experts]
    farmer_embedding = model.encode(farmer.introduction)

    # expert_introductions = [expert.introduction for expert in filtered_experts]
    # farmer_introduction = farmer.introduction

    # expert_keywords = extract_keywords(expert_introductions)
    # farmer_keywords = get_farmer_keywords(farmer_introduction)
    # print(expert_keywords)
    # print(farmer_keywords)
    similarities = [(expert, calculate_similarity(expert_embedding, farmer_embedding))
                    for expert, expert_embedding in zip(filtered_experts, expert_embeddings)]

    # 키워드 유사도 계산
    # similarities = [
    #     (expert, compare_keywords(expert_kw, farmer_keywords))
    #     for expert, expert_kw in zip(filtered_experts, expert_keywords)
    # ]

    # 유사도 기준으로 내림차순 정렬
    sorted_experts = sorted(similarities, key=lambda x: x[1], reverse=True)

    # 상위 4개의 전문가만 반환
    # top_4_experts = sorted_experts[:6]

    return [ExpertEmbedding(
        id=expert.id,
        job=expert.job,
        career=expert.career,
        image=f"/local_images/{expert.image % 10 + 1}.jpg",
        title=expert.title,
        price=expert.price,
        introduction=expert.introduction,
        region=expert.region,
        name=db.query(User).filter(User.id == expert.id).first().name,
        similarity=similarity
    ) for expert, similarity in sorted_experts]


def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))


def dummy_data(db: Session):
    # 1. User 생성 (5명)
    # User 생성 (10명)
    users = []
    for i in range(100):
        role = Role.FARMER if i % 2 == 0 else Role.EXPERT  # FARMER와 EXPERT를 번갈아가며 설정
        name = random_name(8)  # 랜덤한 알파벳 8글자 이름 생성
        phone = f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        user = User(name=name, role=role, phone=phone)
        users.append(user)

    # 2. User 레코드를 데이터베이스에 추가하고 커밋
    db.add_all(users)
    db.commit()  # 커밋하여 전문가 데이터를 DB에 저장합니다.

    # 2. FarmerProfile 생성
    expert_profiles = []
    regions = ["서울 강남구", "서울 강북구", "경기 수원시", "부산 해운대구", "대전 유성구"]

    for i in range(100):
        # 직업 랜덤으로 선택
        target = random.choice(list(expert_data.keys()))
        category = random.choice(list(expert_data[target].keys()))
        job = random.choice(expert_data[target][category])

        # 서울 강남구에 5명, 다른 지역에 5명
        region = random.choice(regions)

        expert_profile = ExpertProfile(
            id=users[i].id,  # User의 id를 참조
            image=i + 1,
            career=f"{random.randint(3, 15)}년 이상의 {job} 경험",  # 경험 연도는 3~15년 사이로 랜덤
            job=job,
            region=region,
            title=f"{job} 전문가",
            price=random.randint(30000, 70000),  # 랜덤으로 3만원 ~ 7만원 가격 설정
            introduction=f"{job}로서, {random.choice(['정서적', '신체적', '심리적'])} 문제를 해결하는 전문가입니다."
        )

        expert_profiles.append(expert_profile)

    # 3. ExpertProfile 데이터를 데이터베이스에 추가
    db.add_all(expert_profiles)


    # 커밋
    db.commit()


def main_search(db: Session):
    experts = db.query(ExpertProfile).all()
    expert_list = []
    for _ in range(10):
        expert_list.append(random.choice(experts))

    return [ExpertResponse(
        id=expert.id,
        image=f"/local_images/{expert.image % 10 + 1}.jpg",
        job=expert.job,
        career=expert.career,
        region=expert.region,
        title=expert.title,
        price=expert.price,
        introduction=expert.introduction,
        name=db.query(User).filter(User.id == expert.id).first().name,
        phone=db.query(User).filter(User.id == expert.id).first().phone,
    ) for expert in expert_list]
