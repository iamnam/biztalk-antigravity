"""Upstage Solar-Pro4 모델 기반 업무 말투 변환 서비스 모듈"""

import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.templates import get_system_prompt

# .env 환경변수 로드
load_dotenv()


def convert_tone(text: str, target_audience: str) -> str:
    """
    원문 텍스트를 수신 대상에 맞는 비즈니스 말투로 변환합니다.

    Args:
        text: 변환할 원문 문자열
        target_audience: 수신 대상 코드 ('boss', 'colleague', 'client', 'team')

    Returns:
        변환된 텍스트 문자열
    """
    api_key = os.getenv("UPSTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("UPSTAGE_API_KEY 환경변수가 설정되지 않았습니다.")

    system_prompt = get_system_prompt(target_audience)
    llm = ChatUpstage(api_key=api_key, model_name="solar-pro4")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=text)
    ]

    try:
        response = llm.invoke(messages)
        converted_text = str(response.content).strip()
        # 앞뒤 불필요한 따옴표가 포함된 경우 제거
        if (converted_text.startswith('"') and converted_text.endswith('"')) or \
           (converted_text.startswith("'") and converted_text.endswith("'")):
            converted_text = converted_text[1:-1].strip()
        return converted_text
    except Exception as exc:
        raise RuntimeError(f"Solar LLM 변환 실패: {str(exc)}") from exc
