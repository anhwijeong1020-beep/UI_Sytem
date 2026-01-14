import json
import time
import streamlit as st

st.set_page_config(page_title="Logistics UI", layout="wide")
st.title("📦 Logistics Move Request UI")

st.caption(
    "자연어로 상황을 설명하고, 자재 / 시점 / 종점은 반드시 입력하세요.\n"
    "건물·층·공간 명칭은 자유 입력입니다."
)

with st.form("move_request_form"):
    # 1) Natural language
    st.subheader("1) Natural language request")
    nl = st.text_area(
        "Intent & site situation",
        placeholder=(
            "예) 10층에서 방 C로 목재를 옮기고 싶다.\n"
            "복도 A는 마감 공사 중이라 피하고,\n"
            "가능하면 안전 우선으로 이동하고 싶다."
        ),
        height=140,
    )

    # 2) Mandatory minimal fields
    st.subheader("2) Required fields (must fill)")
    c1, c2, c3 = st.columns(3)

    with c1:
        material = st.text_input(
            "Material (자재) *",
            placeholder="예) 목재 / 석고보드 / 케이블 트레이",
        )
    with c2:
        start = st.text_input(
            "Start (시점) *",
            placeholder="예) 10F 복도 B / 1F 적치장",
        )
    with c3:
        goal = st.text_input(
            "Goal (종점) *",
            placeholder="예) 10F Room C / 7F 기계실",
        )

    # 3) Strategy option
    st.subheader("3) Strategy option")
    strategy = st.radio(
        "Routing strategy",
        [
            "auto",
            "time-first",
            "safety-first",
            "smooth-first",
            "flow-first",
            "cost-first",
        ],
        horizontal=True,
    )

    notes = st.text_area(
        "Extra notes (optional)",
        placeholder="예) 계단 사용 금지, 엘리베이터 혼잡 시간대 등",
        height=90,
    )

    submitted = st.form_submit_button("Generate payload")

# ---- validation & output ----
if submitted:
    missing = []
    if not material.strip():
        missing.append("Material")
    if not start.strip():
        missing.append("Start")
    if not goal.strip():
        missing.append("Goal")

    if missing:
        st.error(
            f"❌ 필수 항목이 비어 있습니다: {', '.join(missing)}\n"
            "자재 / 시점 / 종점은 반드시 입력해야 합니다."
        )
        st.stop()

    payload = {
        "natural_language": nl.strip(),
        "material": material.strip(),
        "start": start.strip(),
        "goal": goal.strip(),
        "strategy": strategy,
        "notes": notes.strip(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ui_version": "nl + required free-text fields + strategy",
    }

    payload_str = json.dumps(payload, ensure_ascii=False, indent=2)

    st.success("✅ Payload generated")
    st.subheader("Payload (JSON)")
    st.code(payload_str, language="json")

    st.download_button(
        "⬇️ Download payload.json",
        data=payload_str.encode("utf-8"),
        file_name="payload.json",
        mime="application/json",
    )

    st.info(
        "이 payload.json을 Colab에 업로드하여\n"
        "전략 해석 / 목적함수 생성 / 경로 최적화 파이썬 코드를 실행하면 됩니다."
    )
