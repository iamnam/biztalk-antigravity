/**
 * 업무 말투 변환기 (BizTalk) — 프론트엔드 비즈니스 로직
 * 바닐라 자바스크립트 (ES6+) 기반 경량 구현
 */

// 동일 도메인(로컬 및 배포 환경) 호환 상대 경로 API 베이스
const API_BASE = window.location.origin;

// 대상별 배지 라벨 매핑
const TARGET_LABELS = {
    boss: "상사 / 임원 톤",
    colleague: "타팀 동료 톤",
    client: "고객 / 외부 톤",
    team: "팀 내 동료 톤"
};

// 예시 문장 목록
const SAMPLE_TEXTS = [
    "내일까지 보고서 제출 어려울 것 같음",
    "지난주 요청드린 데이터 오늘까지 꼭 보내주세요",
    "서버 점검 때문에 오늘 밤 10시부터 사이트 접속이 안 됩니다",
    "이 부분 버그 있는 것 같은데 확인 좀 부탁해"
];

let sampleIndex = 0;

// DOM 엘리먼트 참조
const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const charCount = document.getElementById("charCount");
const convertBtn = document.getElementById("convertBtn");
const copyBtn = document.getElementById("copyBtn");
const exampleBtn = document.getElementById("exampleBtn");
const clearBtn = document.getElementById("clearBtn");
const spinner = document.getElementById("spinner");
const loadingOverlay = document.getElementById("loadingOverlay");
const outputAudienceLabel = document.getElementById("outputAudienceLabel");
const targetButtons = document.querySelectorAll(".target-btn");
const toast = document.getElementById("toast");

/**
 * 토스트 알림 표시
 */
function showToast(message, duration = 2500) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove("hidden");
    
    // 이전 타이머 정리
    if (toast._timer) clearTimeout(toast._timer);
    
    toast._timer = setTimeout(() => {
        toast.classList.add("hidden");
    }, duration);
}

/**
 * 수신 대상 선택 버튼 이벤트 리스너 등록
 */
function initTargetButtons() {
    targetButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            targetButtons.forEach((b) => {
                b.classList.remove("active");
                b.setAttribute("aria-selected", "false");
            });
            btn.classList.add("active");
            btn.setAttribute("aria-selected", "true");
            
            const target = btn.dataset.target;
            if (outputAudienceLabel && TARGET_LABELS[target]) {
                outputAudienceLabel.textContent = TARGET_LABELS[target];
            }
        });
    });
}

/**
 * 현재 선택된 수신 대상 코드 반환
 */
function getSelectedTarget() {
    const activeBtn = document.querySelector(".target-btn.active");
    return activeBtn ? activeBtn.dataset.target : "boss";
}

/**
 * 로딩 상태 전환 (버튼 비활성화, 스피너 및 오버레이 토글)
 */
function setLoading(isLoading) {
    if (isLoading) {
        convertBtn.disabled = true;
        if (spinner) spinner.classList.remove("hidden");
        if (loadingOverlay) loadingOverlay.classList.remove("hidden");
    } else {
        convertBtn.disabled = false;
        if (spinner) spinner.classList.add("hidden");
        if (loadingOverlay) loadingOverlay.classList.add("hidden");
    }
}

/**
 * 말투 변환 API 호출 핵심 함수
 */
async function convertTone() {
    const text = inputText.value.trim();
    const target = getSelectedTarget();

    if (!text) {
        showToast("⚠️ 변환할 내용을 입력해주세요.");
        inputText.focus();
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE}/api/convert`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: text,
                target_audience: target,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const detailMsg = errorData.detail || "변환 서버 오류가 발생했습니다.";
            throw new Error(detailMsg);
        }

        const data = await response.json();
        outputText.value = data.converted_text || "";
        showToast("✨ 업무 말투 변환이 완료되었습니다!");
    } catch (error) {
        console.error("변환 오류:", error);
        showToast(`❌ ${error.message || "변환 중 오류가 발생했습니다. 다시 시도해주세요."}`);
    } finally {
        setLoading(false);
    }
}

/**
 * 클립보드 복사 기능
 */
async function copyToClipboard() {
    const text = outputText.value.trim();
    if (!text) {
        showToast("⚠️ 복사할 변환 결과가 없습니다.");
        return;
    }

    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
        } else {
            // 구형 브라우저 또는 비보안 컨텍스트 폴백
            outputText.select();
            document.execCommand("copy");
        }
        showToast("📋 클립보드에 복사되었습니다!");
    } catch (err) {
        console.error("복사 실패:", err);
        showToast("❌ 복사에 실패했습니다. 직접 복사해주세요.");
    }
}

/**
 * 글자 수 카운터 업데이트
 */
function updateCharCount() {
    if (charCount && inputText) {
        charCount.textContent = inputText.value.length;
    }
}

/**
 * 예시 문장 자동 삽입
 */
function insertSampleText() {
    const sample = SAMPLE_TEXTS[sampleIndex % SAMPLE_TEXTS.length];
    sampleIndex++;
    inputText.value = sample;
    updateCharCount();
    inputText.focus();
    showToast("💡 예시 문장이 입력되었습니다.");
}

/**
 * 텍스트 초기화
 */
function clearInput() {
    inputText.value = "";
    outputText.value = "";
    updateCharCount();
    inputText.focus();
}

/**
 * 키보드 단축키 (Ctrl + Enter 또는 Cmd + Enter)
 */
function handleKeyDown(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        convertTone();
    }
}

// 초기 이벤트 리스너 바인딩
document.addEventListener("DOMContentLoaded", () => {
    initTargetButtons();
    
    if (convertBtn) convertBtn.addEventListener("click", convertTone);
    if (copyBtn) copyBtn.addEventListener("click", copyToClipboard);
    if (exampleBtn) exampleBtn.addEventListener("click", insertSampleText);
    if (clearBtn) clearBtn.addEventListener("click", clearInput);
    if (inputText) {
        inputText.addEventListener("input", updateCharCount);
        inputText.addEventListener("keydown", handleKeyDown);
    }
});
