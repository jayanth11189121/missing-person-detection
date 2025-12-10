from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
from pathlib import Path
import os
from typing import Optional, List
import uuid
from datetime import datetime
import base64

from backend.detection import FaceDetector
from backend.database import Database

app = FastAPI(title="Missing Person Detection API")

app.mount("/static", StaticFiles(directory="public"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

detector = FaceDetector()
db = Database()

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path("public/index.html")
    if html_path.exists():
        return FileResponse(html_path)
    return {"message": "Missing Person Detection API", "status": "running"}

@app.get("/{file_name}.{file_ext}")
async def serve_static_files(file_name: str, file_ext: str):
    file_path = Path(f"public/{file_name}.{file_ext}")
    if file_path.exists():
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/api/missing-persons")
async def get_missing_persons(status: Optional[str] = "active"):
    try:
        persons = await db.get_missing_persons(status)
        return {"success": True, "data": persons}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/missing-persons")
async def create_missing_person(
    name: str = Form(...),
    description: str = Form(""),
    reference_image: UploadFile = File(...)
):
    try:
        image_data = await reference_image.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        image_filename = f"{uuid.uuid4()}.jpg"
        image_path = UPLOAD_DIR / image_filename
        cv2.imwrite(str(image_path), image)

        person_id = await db.create_missing_person(
            name=name,
            description=description,
            reference_image_url=str(image_path)
        )

        return {
            "success": True,
            "data": {
                "id": person_id,
                "name": name,
                "reference_image_url": str(image_path)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect/video")
async def detect_in_video(
    missing_person_id: str = Form(...),
    video: UploadFile = File(...)
):
    try:
        person = await db.get_missing_person_by_id(missing_person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Missing person not found")

        video_data = await video.read()
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = UPLOAD_DIR / video_filename

        with open(video_path, "wb") as f:
            f.write(video_data)

        ref_image = cv2.imread(person["reference_image_url"])
        if ref_image is None:
            raise HTTPException(status_code=400, detail="Reference image not found")

        result = await detector.detect_in_video(
            reference_image=ref_image,
            video_path=str(video_path),
            person_name=person["name"]
        )

        if result["detected"]:
            detection_id = await db.create_detection(
                missing_person_id=missing_person_id,
                detection_type="video",
                confidence_score=result["confidence"],
                frame_url=result["frame_path"],
                video_url=result["output_video_path"]
            )

            return {
                "success": True,
                "detected": True,
                "data": {
                    "detection_id": detection_id,
                    "confidence": result["confidence"],
                    "frame_url": result["frame_path"],
                    "video_url": result["output_video_path"]
                }
            }
        else:
            return {
                "success": True,
                "detected": False,
                "message": "Person not found in video"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/detections/{missing_person_id}")
async def get_detections(missing_person_id: str):
    try:
        detections = await db.get_detections_by_person(missing_person_id)
        return {"success": True, "data": detections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/file/{file_path:path}")
async def get_file(file_path: str):
    full_path = Path(file_path)
    if full_path.exists():
        return FileResponse(full_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
