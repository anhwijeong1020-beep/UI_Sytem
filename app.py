import json
import streamlit as st

st.set_page_config(page_title="Logistics UI", layout="wide")
st.title("📦 Construction Logistics - Input UI")

FLOORS = ["5F", "10F"]
NODES = ["Entrance_1", "Corridor_A", "Corridor_B", "Room_A", "Room_C", "Storage_1"]
ZONES = ["Corridor_A", "Stair_1", "Elevator_1", "Narrow_Passage", "Work_Area_1"]

with st.form("scenario_form"):
    st.subheader("1) Natural language (optional)")
    nl = st.text_area(
        "Request",
        placeholder="e.g., Move wood to Room C, avoid Corridor A, prioritize safety.",
        height=100,
    )

    st.subheader("2) Location")
    c1, c2, c3 = st.columns(3)
    with c1:
        floor = st.selectbox("Floor", FLOORS)
    with c2:
        start = st.selectbox("Start", NODES)
    with c3:
        goal = st.selectbox("Goal", NODES)

    st.subheader("3) Constraints")
    avoid = st.multiselect("Avoid zones", ZONES)

    c4, c5, c6 = st.columns(3)
    with c4:
        elevator_allowed = st.checkbox("Elevator allowed", value=True)
    with c5:
        stairs_allowed = st.checkbox("Stairs allowed", value=False)
    with c6:
        min_width_m = st.number_input("Min corridor width (m)", 0.5, 5.0, 1.2, 0.1)

    st.subheader("4) Objective")
    time_w = st.slider("Time weight", 0.0, 1.0, 0.4, 0.05)
    risk_w = round(1.0 - time_w, 2)

    submitted = st.form_submit_button("Generate payload")

if submitted:
    payload = {
        "natural_language": nl,
        "floor": floor,
        "start": start,
        "goal": goal,
        "constraints": {
            "avoid_zones": avoid,
            "elevator_allowed": elevator_allowed,
            "stairs_allowed": stairs_allowed,
            "min_width_m": float(min_width_m),
        },
        "objective": {"time": round(time_w, 2), "risk": risk_w},
    }

    payload_str = json.dumps(payload, ensure_ascii=False, indent=2)
    st.success("✅ Payload generated")
    st.code(payload_str, language="json")

    st.download_button(
        "⬇️ Download payload.json",
        payload_str.encode("utf-8"),
        "payload.json",
        "application/json",
    )
