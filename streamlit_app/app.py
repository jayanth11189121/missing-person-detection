import streamlit as st
import cv2
import numpy as np
from tempfile import NamedTemporaryFile
import os
from deepface import DeepFace
import time

# ============================================================
#                     PREMIUM UI & STYLE
# ============================================================
st.set_page_config(
    page_title="Missing Person Detector",
    page_icon="🔍",
    layout="wide"
)

# ----- Custom UI Styling -----
st.markdown("""
<style>
    /* Floating Header */
    .block-container {padding-top: 2rem;}
    h1 {position: sticky; top: 0; z-index: 999; padding: 10px; background: rgba(0,0,0,0.6);
        backdrop-filter: blur(10px); border-radius: 12px; text-align: center; color: #fff !important; margin-bottom: 25px;}

    /* Dark Mode Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0f24, #001f3f, #003566);
        animation: gradientShift 15s ease infinite;
        background-size: 400% 400%;
    }
    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #050a11;
        border-right: 2px solid #0abdc6;
    }
    [data-testid="stSidebar"] h1, h2, h3 {color: #0abdc6 !important;}

    /* Sidebar logo center */
    .sidebar-logo {text-align: center; padding-top: 15px; padding-bottom: 20px;}

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {justify-content: center; padding: 10px; margin-bottom: 20px;}
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.06);
        color: #dcecff !important;
        font-size: 18px;
        padding: 10px 30px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        transition: 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.2);
        transform: scale(1.05);
    }
    .stTabs [aria-selected="true"] {
        background: #0abdc6 !important;
        color: black !important;
        font-weight: 900;
    }

    /* Glassmorphism upload card */
    .stFileUploader {
        background: rgba(255,255,255,0.06) !important;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Buttons */
    .stButton button, .stDownloadButton button {
        background: linear-gradient(45deg, #0abdc6, #00f5d4);
        color: black; 
        border-radius: 12px;
        border: none;
        padding: 12px 25px;
        font-size: 18px;
        font-weight: 800;
        transition: 0.2s;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00f5d4;
    }

    /* Image & Video Styling */
    img, video {
        border-radius: 12px;
        box-shadow: 0 0 25px #000000aa;
    }
</style>
""", unsafe_allow_html=True)

# ----- Sidebar Logo -----
st.sidebar.markdown("""
<div class='sidebar-logo'>
    <img src='https://cdn-icons-png.flaticon.com/512/3064/3064197.png' width='120'>
</div>
""", unsafe_allow_html=True)

# ----- Theme Switch -----
theme_mode = st.sidebar.radio("Theme Mode", ["Dark Mode", "Light Mode"], index=0)

if theme_mode == "Light Mode":
    st.markdown("""
    <style>
        /* Light Mode Header */
        .block-container {padding-top: 2rem;}
        h1 {position: sticky; top: 0; z-index: 999; padding: 10px; background: rgba(255,255,255,0.9);
            backdrop-filter: blur(10px); border-radius: 12px; text-align: center; color: #333 !important; margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);}

        /* Light Green Background */
        [data-testid="stAppViewContainer"] {
            background: #d0f0c0 !important;
        }

        /* Sidebar light orange */
        [data-testid="stSidebar"] {
            background: #fff2e6; 
            border-right: 2px solid #ff9933;
            box-shadow: 2px 0 10px rgba(255,153,51,0.2);
        }
        [data-testid="stSidebar"] h1, h2, h3 {color: #ff9933 !important;}

        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,200,150,0.15);
            color: #663300 !important;
            font-size: 18px;
            padding: 10px 30px;
            border-radius: 12px;
            border: 1px solid rgba(255,153,51,0.4);
            transition: 0.3s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(255,153,51,0.3); 
            transform: scale(1.08);
            box-shadow: 0 0 15px rgba(255,153,51,0.5);
        }
        .stTabs [aria-selected="true"] {
            background: #ff9933 !important; 
            color: white !important; 
            font-weight: 900;
            box-shadow: 0 0 20px rgba(255,153,51,0.6);
        }

        /* Buttons */
        .stButton button, .stDownloadButton button {
            background: linear-gradient(45deg, #ffb84d, #ff9933);
            color: black; border-radius: 12px; border: none;
            padding: 12px 25px; font-size: 18px; font-weight: 900; transition: 0.3s;
            box-shadow: 0 4px 12px rgba(255,153,51,0.4);
        }
        .stButton button:hover, .stDownloadButton button:hover {
            transform: scale(1.08); 
            box-shadow: 0 0 25px rgba(255,153,51,0.8);
        }

        /* Image & Video */
        img, video {border-radius: 12px; box-shadow: 0 0 25px rgba(0,0,0,0.2);}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
#                     ORIGINAL APP CODE
# ============================================================
st.title("Missing Person Detector")
tabs = st.tabs(["Video Detection", "Live Webcam Detection"])

# -------------------- Feature 1: Video Detection --------------------
with tabs[0]:
    st.header(" Detect Person in Video")
    uploaded_images = st.file_uploader(
        "Upload reference image (person to track) for Video Detection",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"],
        key="video_ref"
    )
    uploaded_video = st.file_uploader(
        "Upload video",
        type=["mp4", "avi", "mov"],
        key="video_upload"
    )

    if uploaded_images and uploaded_video:
        st.info("Processing video, please wait...")
        img_file = uploaded_images[0]
        file_bytes = np.frombuffer(img_file.read(), np.uint8)
        ref_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        ref_embedding = DeepFace.represent(img_path=ref_image, model_name="Facenet", enforce_detection=True)[0]["embedding"]
        person_name = img_file.name.split(".")[0]

        tfile = NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_video.read())
        tfile_path = tfile.name

        video_capture = cv2.VideoCapture(tfile_path)
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_path = os.path.join(os.getcwd(), "output_video_fast.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        detected = False
        detected_face_img = None
        detected_frame = None
        frame_skip = 5
        current_frame = 0
        progress_bar = st.progress(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            current_frame += 1
            progress_bar.progress(current_frame / int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT)))
            if current_frame % frame_skip != 0 and not detected:
                out_video.write(frame)
                continue
            if not detected:
                small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
                try: results = DeepFace.extract_faces(img_path=small_frame, enforce_detection=False)
                except: results = []
                best_similarity = 0
                best_face = None
                x, y, w, h = 0, 0, 0, 0
                for face in results:
                    fx = int(face["facial_area"]["x"] * 2)
                    fy = int(face["facial_area"]["y"] * 2)
                    fw = int(face["facial_area"]["w"] * 2)
                    fh = int(face["facial_area"]["h"] * 2)
                    face_img = frame[fy:fy+fh, fx:fx+fw]
                    embedding = DeepFace.represent(img_path=face_img, model_name="Facenet", enforce_detection=False)[0]["embedding"]
                    cos_sim = np.dot(ref_embedding, embedding) / (np.linalg.norm(ref_embedding) * np.linalg.norm(embedding))
                    if cos_sim > best_similarity:
                        best_similarity = cos_sim
                        best_face = face_img
                        x, y, w, h = fx, fy, fw, fh
                if best_similarity > 0.7:
                    detected = True
                    detected_face_img = best_face
                    detected_frame = frame.copy()
                    cv2.rectangle(detected_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(detected_frame, person_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            out_video.write(detected_frame if detected else frame)

        if detected_frame is not None:
            for _ in range(fps * 3):
                out_video.write(detected_frame)
        video_capture.release()
        out_video.release()

        if detected:
            st.success(f"{person_name} found in video!")
            st.image(detected_face_img, caption=f"{person_name} detected!", use_column_width=True)
        else:
            st.warning("Person not found in video!")
        st.video(output_path)
        st.download_button("Download Processed Video", data=open(output_path, "rb"), file_name="output_video_fast.mp4")

# -------------------- Feature 2: Live Webcam Detection --------------------
with tabs[1]:
    st.header(" Detect Person via Live Webcam (Fast)")
    webcam_ref_image = st.file_uploader(
        "Upload reference image (person to track) for Webcam Detection",
        type=["jpg", "jpeg", "png"],
        key="webcam_ref"
    )
    if webcam_ref_image:
        file_bytes = np.frombuffer(webcam_ref_image.read(), np.uint8)
        webcam_ref = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        webcam_ref_embedding = DeepFace.represent(img_path=webcam_ref, model_name="Facenet", enforce_detection=True)[0]["embedding"]
        webcam_person_name = webcam_ref_image.name.split(".")[0]
        st.info("Starting webcam... (close webcam window to stop)")
        cap = cv2.VideoCapture(0)
        webcam_placeholder = st.empty()
        detected_webcam_face = None
        detected_webcam_frame = None
        detected_webcam = False
        frame_skip = 2
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frame_count += 1
            if frame_count % frame_skip == 0 and not detected_webcam:
                small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
                try: results = DeepFace.extract_faces(img_path=small_frame, enforce_detection=False)
                except: results = []
                best_similarity = 0
                for face in results:
                    fx = int(face["facial_area"]["x"] / 0.5)
                    fy = int(face["facial_area"]["y"] / 0.5)
                    fw = int(face["facial_area"]["w"] / 0.5)
                    fh = int(face["facial_area"]["h"] / 0.5)
                    face_img = frame[fy:fy+fh, fx:fx+fw]
                    embedding = DeepFace.represent(img_path=face_img, model_name="Facenet", enforce_detection=False)[0]["embedding"]
                    cos_sim = np.dot(webcam_ref_embedding, embedding) / (np.linalg.norm(webcam_ref_embedding) * np.linalg.norm(embedding))
                    if cos_sim > best_similarity:
                        best_similarity = cos_sim
                        detected_webcam_face = face_img
                        detected_webcam_frame = frame.copy()
                        x, y, w, h = fx, fy, fw, fh
                if best_similarity > 0.7:
                    detected_webcam = True
                    cv2.rectangle(detected_webcam_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(detected_webcam_frame, webcam_person_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    for _ in range(30):
                        webcam_placeholder.image(cv2.cvtColor(detected_webcam_frame, cv2.COLOR_BGR2RGB))
                        time.sleep(0.1)
            webcam_placeholder.image(cv2.cvtColor(detected_webcam_frame if detected_webcam else frame, cv2.COLOR_BGR2RGB))
        cap.release()
        if detected_webcam:
            st.success(f"{webcam_person_name} detected in webcam!")
            st.image(detected_webcam_face, caption=f"{webcam_person_name} detected!", use_column_width=True)
        else:
            st.warning(f"{webcam_person_name} not detected in webcam.")

# ============================================================
#                     PREMIUM FOOTER
# ============================================================
st.markdown("""
<br><br>
<div style='text-align:center; padding:20px; color:#333;'>
    <hr style='border-color:#0abdc6;'/>
    <h3 style='color:#0abdc6;'>🔍 Missing Person Detector</h3>
    <p style='font-size:15px;'>
        Powered by DeepFace • Designed for Speed, Accuracy & Presentation
    </p>
    <p style='font-size:13px; color:#7ac7ff;'>© 2025 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
