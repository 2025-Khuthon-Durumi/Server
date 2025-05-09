import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.domain.expert import expert_router
from app.domain.farmer import farmer_router
from app.domain.order import order_router
from app.domain.user import user_router

app = FastAPI()

origins = [
    "*",
]

app.include_router(user_router.router)
app.include_router(expert_router.router)
app.include_router(order_router.router)
app.include_router(farmer_router.router)

IMAGE_DIRECTORY = "local_images"
app.mount("/local_images", StaticFiles(directory=IMAGE_DIRECTORY), name="images")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


from sentence_transformers import SentenceTransformer, util
import pandas as pd

from pydantic import BaseModel


class IntroInput(BaseModel):
    text: str
    number: int


@app.post("/recommend-expert")
def recommend_api(data: IntroInput):
    """
    # 혼자 테스트용, 사용 X
    """
    return recommend_expert_bert(data.text, data.number)


# ✅ 모델 불러오기 (한국어용 BERT)
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")


def recommend_expert_bert(intro: str, n: int = 3):
    # 1. 전문가 목록 불러오기
    df = pd.read_csv("experts.csv")
    expert_texts = df["설명"].tolist()

    # 2. 소개글과 전문가 설명 전체를 임베딩
    embeddings = model.encode([intro] + expert_texts, convert_to_tensor=True)

    # 3. 첫 번째 임베딩(자기소개)과 나머지 임베딩(전문가 설명)의 유사도 계산
    similarities = util.cos_sim(embeddings[0], embeddings[1:]).cpu().numpy()[0]

    # 4. 유사도 높은 순으로 정렬
    top_indices = similarities.argsort()[::-1][:n]

    # 5. 상위 N개 전문가 정보 반환
    return df.iloc[top_indices][["이름", "전문 분야", "설명"]].to_dict(orient="records")
