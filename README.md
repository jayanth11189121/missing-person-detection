# LensLock - Pro Version (Option B)

**What this repo contains (Pro):**
- Upload image + upload video or RTSP live input
- YOLOv8 person detection
- Full-body ReID (OSNet-like via ResNet50 backbone placeholder)
- DeepSort tracking integration (placeholder integration)
- FAISS-based fast similarity search
- FastAPI backend for video processing + report generation
- Streamlit frontend (multi-panel) with Upload, Live RTSP, and Reports
- Export match report (JSON + PDF)

**Notes:**
- This scaffold focuses on functionality and hackathon readiness. Replace placeholders with optimized ReID models (OSNet / FastReID) and tune for GPU to get production speeds.
- Place `yolov8n.pt` inside `backend/models/`
- Place ReID model weights inside `backend/models/` (optional)
- For RTSP tests ensure the RTSP stream is accessible from the machine running the backend.

**Quickstart**
1. Create virtualenv and activate it.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Start backend:
   ```bash
   uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
   ```
4. In another terminal, run frontend:
   ```bash
   streamlit run streamlit_app/app.py
   ```
5. Open Streamlit UI and try Upload or RTSP workflows.

**What's next?**
- Add GPU optimized ReID (OSNet / FastReID)
- Add background job queue (Redis + RQ/Celery)
- Add authentication and database for saved results
