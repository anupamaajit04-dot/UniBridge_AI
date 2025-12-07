import streamlit as st
import cv2
from video_module import init_video, analyze_video_frame

st.title("UniBridge – Disaster Risk Dashboard")

st.subheader("Sensor Panel")

water_level = st.slider("Water Level (cm)", 0, 200, 50)
rainfall = st.slider("Rainfall (mm)", 0, 100, 10)

st.write("Water level:", water_level)
st.write("Rainfall:", rainfall)

st.subheader("Camera Panel")

if "cap" not in st.session_state:
    st.session_state["cap"] = init_video("flood.mp4")

cap = st.session_state["cap"]

frame, video_flag = analyze_video_frame(cap)

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
st.image(frame_rgb, channels="RGB", caption=f"Camera status: {video_flag}")

# DEBUG: show whether video opened
st.write("Video status:", cap.isOpened())


def compute_risk(water_level, rainfall, video_flag):
    if water_level > 120 and rainfall > 40:
        base = "HIGH"
    elif water_level > 120 or rainfall > 40:
        base = "MEDIUM"
    else:
        base = "LOW"

    if base == "MEDIUM" and video_flag == "flood":
        return "HIGH"
    return base

risk = compute_risk(water_level, rainfall, video_flag)

st.subheader("Overall Risk")

if risk == "LOW":
    st.success("LOW")
elif risk == "MEDIUM":
    st.warning("MEDIUM")
else:
    st.error("HIGH")
