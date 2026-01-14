import json
import time
import streamlit as st

st.set_page_config(page_title="Logistics UI", layout="wide")
st.title("📦 Logistics Move Request UI")

st.caption("자연어로 상황을 설명하고, 자재/시점/종점만 최소 정보로 입력하세요. (건물/층/방 명칭은 자유 입력)")

with st.form("move_request_form"):
    st.subheader("1) Natural language request (main)")
    nl = st.text_area(
        "Describe your intent & site situation",
        placeholder=(
            "예) 10층에서 방 C로 목재를 옮기고 싶어.\n"
            "복도 A는 마감 작업 중이라 피하고,\n"
            "가능하면 안전 우선으로 가고 싶어."
        ),
        height=140,
    )

    st.subheader("2) Minimal structured fields (free text)")
    c1, c2, c3 = st.columns(3)
    with c1:
        material = st.text_input(
            "Material (자재)",
            placeholder="예) 목재 / 석고보드 / 타일 / 케이블트레이",
        )
    with c2:
        start = st.text_input(
            "Start (시점)",
            placeholder="예) 10F 복도 B / 5F 엘리베이터홀 / 1F 적치장",
        )
    with c3:
        goal = st.text_input(
            "Goal (종점)",
            placeholder="예) 10F Room C / 7F 기계실 / 3F 작업면",
        )

    st.subheader("3) Optional (if you want)")
    priority = st.radio(
        "Preferred priority (선호)",
        ["auto (let system decide)", "safety-first", "time-first", "balanced"],
        horizontal=True,
    )

    notes = st.text_area(
        "Extra notes (optional)",
        placeholder="예) 계단 사용 금지, 엘리베이터 혼잡 시간대, 폭 제한 우려 등",
        height=90,
    )

    submitted = st.form_submit_button("Generate payload")

if submitted:
    # 최소 입력 검증(너무 빡세게 막지 않기)
    warnings = []
    if not nl.strip():
        warnings.append("자연어 설명이 비어있어요. (그래도 진행은 가능)")
    if not material.strip():
        warnings.append("자재(Material)가 비어있어요.")
    if not start.strip():
        warnings.append("시점(Start)가 비어있어요.")
    if not goal.strip():
        warnings.append("종점(Goal)가 비어있어요.")

    payload = {
        "natural_language": nl.strip(),
        "material": material.strip(),
        "start": start.strip(),
        "goal": goal.strip(),
        "priority_hint": priority,
        "notes": notes.strip(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ui_version": "nl + 3 free-text fields",
        "warnings": warnings,
    }

    st.success("✅ Payload generated")
    if warnings:
        st.warning(" / ".join(warnings))

    payload_str = json.dumps(payload, ensure_ascii=False, indent=2)
    st.subheader("Payload (JSON)")
    st.code(payload_str, language="json")

    st.download_button(
        "⬇️ Download payload.json",
        data=payload_str.encode("utf-8"),
        file_name="payload.json",
        mime="application/json",
    )

    st.info("이 payload.json을 Colab에 업로드해서 해석/전략결정/경로계획 파이썬 코드를 실행하면 됩니다.")
