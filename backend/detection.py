import cv2
import numpy as np
from pathlib import Path
import os
from deepface import DeepFace
from typing import Dict, Optional
import uuid

class FaceDetector:
    def __init__(self, model_name: str = "Facenet"):
        self.model_name = model_name
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)

    def get_face_embedding(self, image: np.ndarray) -> Optional[list]:
        try:
            result = DeepFace.represent(
                img_path=image,
                model_name=self.model_name,
                enforce_detection=True
            )
            return result[0]["embedding"]
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def calculate_similarity(self, embedding1: list, embedding2: list) -> float:
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        cos_sim = np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
        return float(cos_sim)

    async def detect_in_video(
        self,
        reference_image: np.ndarray,
        video_path: str,
        person_name: str,
        threshold: float = 0.7,
        frame_skip: int = 5
    ) -> Dict:
        ref_embedding = self.get_face_embedding(reference_image)
        if ref_embedding is None:
            return {
                "detected": False,
                "error": "Could not extract face from reference image"
            }

        video_capture = cv2.VideoCapture(video_path)
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        output_filename = f"detected_{uuid.uuid4()}.mp4"
        output_path = self.output_dir / output_filename
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        detected = False
        detected_frame = None
        detected_face_img = None
        best_confidence = 0.0
        current_frame = 0
        detection_frame_num = 0

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            current_frame += 1

            if current_frame % frame_skip == 0 and not detected:
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                try:
                    faces = DeepFace.extract_faces(
                        img_path=small_frame,
                        enforce_detection=False
                    )

                    for face in faces:
                        fx = int(face["facial_area"]["x"] * 2)
                        fy = int(face["facial_area"]["y"] * 2)
                        fw = int(face["facial_area"]["w"] * 2)
                        fh = int(face["facial_area"]["h"] * 2)

                        face_img = frame[fy:fy+fh, fx:fx+fw]
                        if face_img.size == 0:
                            continue

                        face_embedding = self.get_face_embedding(face_img)
                        if face_embedding is None:
                            continue

                        similarity = self.calculate_similarity(ref_embedding, face_embedding)

                        if similarity > threshold and similarity > best_confidence:
                            best_confidence = similarity
                            detected = True
                            detected_face_img = face_img
                            detected_frame = frame.copy()
                            detection_frame_num = current_frame

                            cv2.rectangle(
                                detected_frame,
                                (fx, fy),
                                (fx+fw, fy+fh),
                                (0, 255, 0),
                                3
                            )
                            cv2.putText(
                                detected_frame,
                                f"{person_name} ({similarity:.2f})",
                                (fx, fy-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (0, 255, 0),
                                2
                            )
                except Exception as e:
                    print(f"Error processing frame {current_frame}: {e}")

            out_video.write(detected_frame if detected else frame)

        if detected and detected_frame is not None:
            for _ in range(fps * 3):
                out_video.write(detected_frame)

        video_capture.release()
        out_video.release()

        frame_path = None
        if detected_face_img is not None:
            frame_filename = f"frame_{uuid.uuid4()}.jpg"
            frame_path = self.output_dir / frame_filename
            cv2.imwrite(str(frame_path), detected_frame)

        return {
            "detected": detected,
            "confidence": best_confidence,
            "frame_number": detection_frame_num,
            "total_frames": total_frames,
            "frame_path": str(frame_path) if frame_path else None,
            "output_video_path": str(output_path)
        }

    async def detect_in_image(
        self,
        reference_image: np.ndarray,
        test_image: np.ndarray,
        threshold: float = 0.7
    ) -> Dict:
        ref_embedding = self.get_face_embedding(reference_image)
        if ref_embedding is None:
            return {
                "detected": False,
                "error": "Could not extract face from reference image"
            }

        try:
            faces = DeepFace.extract_faces(
                img_path=test_image,
                enforce_detection=False
            )

            best_match = None
            best_confidence = 0.0

            for face in faces:
                fx = face["facial_area"]["x"]
                fy = face["facial_area"]["y"]
                fw = face["facial_area"]["w"]
                fh = face["facial_area"]["h"]

                face_img = test_image[fy:fy+fh, fx:fx+fw]
                if face_img.size == 0:
                    continue

                face_embedding = self.get_face_embedding(face_img)
                if face_embedding is None:
                    continue

                similarity = self.calculate_similarity(ref_embedding, face_embedding)

                if similarity > threshold and similarity > best_confidence:
                    best_confidence = similarity
                    best_match = {
                        "x": fx,
                        "y": fy,
                        "w": fw,
                        "h": fh,
                        "confidence": similarity
                    }

            return {
                "detected": best_match is not None,
                "confidence": best_confidence,
                "face_location": best_match
            }
        except Exception as e:
            return {
                "detected": False,
                "error": str(e)
            }
