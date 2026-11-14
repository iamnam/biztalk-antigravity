"""백엔드 API 자동화 검증 스크립트"""

import sys
from pathlib import Path

# backend 디렉토리를 sys.path에 추가
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200, f"Health check failed: {response.text}"
    assert response.json() == {"status": "ok"}
    print("PASS: GET /health")


def test_static_page():
    response = client.get("/")
    assert response.status_code == 200, f"Static page failed: {response.text}"
    assert "업무 말투 변환기" in response.text
    print("PASS: GET / (Static Page index.html)")


def test_swagger_docs():
    response = client.get("/docs")
    assert response.status_code == 200, f"Swagger docs failed: {response.text}"
    print("PASS: GET /docs (Swagger UI)")


def test_convert_validation_error():
    # 유효하지 않은 target_audience
    response = client.post("/api/convert", json={
        "text": "테스트",
        "target_audience": "unknown"
    })
    assert response.status_code == 422, f"Validation test failed: {response.status_code}"

    # 빈 문자열
    response_empty = client.post("/api/convert", json={
        "text": "   ",
        "target_audience": "boss"
    })
    assert response_empty.status_code == 422, f"Validation test failed: {response_empty.status_code}"
    print("PASS: POST /api/convert (Validation 422 Handling)")


def test_convert_boss():
    payload = {
        "text": "내일까지 보고서 제출 어려울 것 같음",
        "target_audience": "boss"
    }
    response = client.post("/api/convert", json=payload)
    assert response.status_code == 200, f"Convert boss failed: {response.text}"
    data = response.json()
    assert "converted_text" in data and len(data["converted_text"]) > 5
    assert data["target_audience"] == "boss"
    assert data["original_text"] == payload["text"]
    print(f"PASS: POST /api/convert (boss) -> 결과: {data['converted_text']}")


def test_convert_team():
    payload = {
        "text": "이거 버그 있는 것 같은데 확인 좀 부탁해",
        "target_audience": "team"
    }
    response = client.post("/api/convert", json=payload)
    assert response.status_code == 200, f"Convert team failed: {response.text}"
    data = response.json()
    assert "converted_text" in data and len(data["converted_text"]) > 5
    assert data["target_audience"] == "team"
    print(f"PASS: POST /api/convert (team) -> 결과: {data['converted_text']}")


def test_convert_colleague():
    payload = {
        "text": "지난주 요청드린 데이터 오늘까지 보내주세요",
        "target_audience": "colleague"
    }
    response = client.post("/api/convert", json=payload)
    assert response.status_code == 200, f"Convert colleague failed: {response.text}"
    data = response.json()
    assert data["target_audience"] == "colleague"
    print(f"PASS: POST /api/convert (colleague) -> 결과: {data['converted_text']}")


def test_convert_client():
    payload = {
        "text": "서버 점검 때문에 오늘 밤 10시부터 사이트 안 됩니다",
        "target_audience": "client"
    }
    response = client.post("/api/convert", json=payload)
    assert response.status_code == 200, f"Convert client failed: {response.text}"
    data = response.json()
    assert data["target_audience"] == "client"
    print(f"PASS: POST /api/convert (client) -> 결과: {data['converted_text']}")


if __name__ == "__main__":
    print("=== 백엔드 통합 검증 시작 ===")
    test_health_check()
    test_static_page()
    test_swagger_docs()
    test_convert_validation_error()
    test_convert_boss()
    test_convert_colleague()
    test_convert_client()
    test_convert_team()
    print("=== 모든 백엔드 검증 통과 ===")
