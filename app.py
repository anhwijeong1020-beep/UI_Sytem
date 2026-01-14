import json
import time
import streamlit as st

st.set_page_config(page_title="Logistics Chat UI", layout="centered")
st.title("💬 Logistics Planner (Chat UI)")

# --- session state init ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 자재 이동 요청을 자연어로 입력해줘. (예: '10층에서 방 C로 목재 옮기고, 복도 A는 피하고, 안전 우선')"}
    ]

# --- render chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- chat input ---
user_text = st.chat_input("여기에 자연어로 입력하세요...")

if user_text:
    # show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    # assistant placeholder response (아직 LLM/해석 연결 전)
    with st.chat_message("assistant"):
        with st.spinner("입력을 저장 중..."):
            time.sleep(0.4)
        st.write("✅ 입력을 받았어! 아래에서 payload로 저장/다운로드할 수 있어.")

    st.session_state.messages.append(
        {"role": "assistant", "content": "✅ 입력을 받았어! 아래에서 payload로 저장/다운로드할 수 있어."}
    )

# --- payload 생성: 가장 최근 user 메시지 ---
latest_user = None
for m in reversed(st.session_state.messages):
    if m["role"] == "user":
        latest_user = m["content"]
        break

st.divider()
st.subheader("📦 Payload export")

if latest_user is None:
    st.info("아직 사용자 입력이 없어요. 위 채팅창에 먼저 입력해줘!")
else:
    payload = {
        "natural_language": latest_user,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ui": "streamlit_chat",
    }
    payload_str = json.dumps(payload, ensure_ascii=False, indent=2)

    st.code(payload_str, language="json")

    st.download_button(
        "⬇️ Download payload.json",
        data=payload_str.encode("utf-8"),
        file_name="payload.json",
        mime="application/json",
    )

    # 대화 전체도 저장하고 싶으면
    full_payload = {
        "conversation": st.session_state.messages,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ui": "streamlit_chat",
    }
    full_str = json.dumps(full_payload, ensure_ascii=False, indent=2)

    with st.expander("대화 전체(JSON) 다운로드"):
        st.code(full_str, language="json")
        st.download_button(
            "⬇️ Download conversation.json",
            data=full_str.encode("utf-8"),
            file_name="conversation.json",
            mime="application/json",
        )
