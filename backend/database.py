import os
from supabase import create_client, Client
from typing import Optional, List, Dict
from datetime import datetime

class Database:
    def __init__(self):
        supabase_url = os.getenv("VITE_SUPABASE_URL")
        supabase_key = os.getenv("VITE_SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("Supabase credentials not found in environment variables")

        self.client: Client = create_client(supabase_url, supabase_key)

    async def create_missing_person(
        self,
        name: str,
        description: str,
        reference_image_url: str
    ) -> str:
        result = self.client.table("missing_persons").insert({
            "name": name,
            "description": description,
            "reference_image_url": reference_image_url,
            "status": "active"
        }).execute()

        return result.data[0]["id"]

    async def get_missing_persons(self, status: Optional[str] = None) -> List[Dict]:
        query = self.client.table("missing_persons").select("*")

        if status:
            query = query.eq("status", status)

        result = query.order("created_at", desc=True).execute()
        return result.data

    async def get_missing_person_by_id(self, person_id: str) -> Optional[Dict]:
        result = self.client.table("missing_persons").select("*").eq("id", person_id).maybeSingle().execute()
        return result.data

    async def update_missing_person_status(self, person_id: str, status: str) -> bool:
        result = self.client.table("missing_persons").update({
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", person_id).execute()

        return len(result.data) > 0

    async def create_detection(
        self,
        missing_person_id: str,
        detection_type: str,
        confidence_score: float,
        frame_url: Optional[str] = None,
        video_url: Optional[str] = None,
        location_info: Optional[Dict] = None
    ) -> str:
        result = self.client.table("detections").insert({
            "missing_person_id": missing_person_id,
            "detection_type": detection_type,
            "confidence_score": confidence_score,
            "frame_url": frame_url,
            "video_url": video_url,
            "location_info": location_info or {}
        }).execute()

        return result.data[0]["id"]

    async def get_detections_by_person(self, missing_person_id: str) -> List[Dict]:
        result = self.client.table("detections").select("*").eq(
            "missing_person_id", missing_person_id
        ).order("detected_at", desc=True).execute()

        return result.data

    async def get_all_detections(self, limit: int = 50) -> List[Dict]:
        result = self.client.table("detections").select(
            "*, missing_persons(name, reference_image_url)"
        ).order("detected_at", desc=True).limit(limit).execute()

        return result.data

    async def create_report(
        self,
        missing_person_id: str,
        report_data: Dict,
        pdf_url: Optional[str] = None
    ) -> str:
        result = self.client.table("detection_reports").insert({
            "missing_person_id": missing_person_id,
            "report_data": report_data,
            "pdf_url": pdf_url
        }).execute()

        return result.data[0]["id"]

    async def get_reports_by_person(self, missing_person_id: str) -> List[Dict]:
        result = self.client.table("detection_reports").select("*").eq(
            "missing_person_id", missing_person_id
        ).order("generated_at", desc=True).execute()

        return result.data
