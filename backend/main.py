"""FastAPI 메인 애플리케이션 진입점"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.convert import router as convert_router

app = FastAPI(
    title="업무 말투 변환기 API",
    description="일상적인 문장을 4가지 대상별 비즈니스 어조로 변환하는 백엔드 API 서비스",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록 (/api)
app.include_router(convert_router, prefix="/api")


# Health Check 엔드포인트
@app.get("/health", tags=["Health"])
async def health_check():
    """서버 헬스 체크 엔드포인트"""
    return {"status": "ok"}


# 프론트엔드 정적 파일 서빙 마운트
# backend/main.py 기준 프로젝트 루트의 frontend 폴더 경로 계산
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
