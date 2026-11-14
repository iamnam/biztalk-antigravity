"""말투 변환 API 라우터 모듈"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import ConvertRequest, ConvertResponse
from services.tone_converter import convert_tone

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Tone Conversion"])


@router.post(
    "/convert",
    response_model=ConvertResponse,
    status_code=status.HTTP_200_OK,
    summary="업무 말투 변환",
    description="원문 텍스트와 수신 대상을 입력받아 비즈니스 업무 말투로 변환합니다."
)
def convert_text(request: ConvertRequest) -> ConvertResponse:
    """
    원문을 지정된 수신 대상의 어조로 변환합니다.
    (동기 함수로 선언되어 FastAPI의 기본 threadpool에서 안전하게 비차단 실행됩니다)
    """
    clean_text = request.text.strip()
    if not clean_text:
        raise HTTPException(
            status_code=422,
            detail="text 필드는 공백을 제외하고 1자 이상이어야 합니다."
        )

    try:
        converted_text = convert_tone(
            text=clean_text,
            target_audience=request.target_audience
        )
        return ConvertResponse(
            converted_text=converted_text,
            target_audience=request.target_audience,
            original_text=clean_text
        )
    except Exception as exc:
        logger.error(f"말투 변환 처리 중 오류 발생: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM API 호출 중 오류가 발생했습니다."
        )
