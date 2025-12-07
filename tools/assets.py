
from typing import Optional
from supabase_client import fetch_rows, insert_row, update_row
from tools.auth import require_role
from tools.activity import log_activity
from datetime import datetime, timezone


def list_assets(status: str = "pending") -> list[dict]:
    """
    Fetch assets with a specific status.
    """
    return fetch_rows("assets", {"status": status})


def upload_asset(requester_email: str, asset_url: str, description: str, related_campaign_id: Optional[str] = None) -> dict:
    """
    Upload an asset record. Team members can upload.
    """
    # All roles can upload (Team, Manager, Admin)
    # So we just check if user exists/has any role? 
    # Spec: "team: can ... upload assets". Implies everyone can.
    
    data = {
        "requester_email": requester_email,
        "file_url": asset_url,
        "description": description,
        "related_campaign_id": related_campaign_id,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    result = insert_row("assets", data)
    
    if result:
        log_activity(requester_email, "upload_asset", "asset", result.get("id", "unknown"), {"url": asset_url})
        
    return result


def review_asset(asset_id: str, reviewer_email: str, decision: str, notes: Optional[str] = None) -> dict:
    """
    Review an asset (approve/reject). Manager/Admin only.
    """
    require_role(reviewer_email, ["admin", "manager"])
    
    data = {
        "status": decision,
        "reviewer_email": reviewer_email,
        "review_notes": notes,
        "reviewed_at": datetime.now(timezone.utc).isoformat()
    }
    result = update_row("assets", {"id": asset_id}, data)
    
    if result:
        log_activity(reviewer_email, "review_asset", "asset", asset_id, {"decision": decision})
        
    return result
