
from supabase_client import fetch_rows, insert_row, update_row
from tools.auth import require_role
from tools.activity import log_activity
from datetime import datetime, timezone


def list_campaigns(status: str = "active") -> list[dict]:
    """
    Fetch campaigns from Supabase table "campaigns" where status matches the input.
    """
    # All roles can list campaigns (Team can list, Manager/Admin can list)
    # Spec says: "team: can only list_campaigns." -> Implies they can see all? 
    # Or "team: can view own tasks, assigned campaigns". 
    # But list_campaigns spec says "Fetch campaigns... where status = input".
    # Let's assume for now list_campaigns returns all matching status.
    return fetch_rows("campaigns", {"status": status})


def create_campaign(name: str, channel: list[str], start_date: str, end_date: str, owner_email: str) -> dict:
    """
    Create a new campaign. Only Admin/Manager.
    """
    # Check permissions (caller must be admin or manager)
    # Wait, how do we know who is calling? The tool args don't include caller email.
    # The spec says: "create_campaign(..., owner_email: str)". 
    # Usually in MCP, the client sends the user identity or we pass it as arg.
    # The spec for create_campaign has `owner_email`. 
    # But `require_role` needs the *caller's* email to check permissions.
    # The prompt implies we should check role based on some email.
    # "Tools like create_campaign... must check role".
    # "create_campaign(..., owner_email: str)".
    # If the `owner_email` is the creator, we check that.
    # Let's assume `owner_email` is the one performing the action or we trust it matches the authenticated user.
    # In a real MCP, we might get a context, but here we just take it as arg.
    
    require_role(owner_email, ["admin", "manager"])
    
    data = {
        "name": name,
        "channel": channel,
        "start_date": start_date,
        "end_date": end_date,
        "owner_email": owner_email,
        "status": "planned",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    result = insert_row("campaigns", data)
    
    # Log activity
    if result:
        log_activity(owner_email, "create_campaign", "campaign", result.get("id", "unknown"), {"name": name})
        
    return result


def update_campaign_status(campaign_id: str, new_status: str, user_email: str) -> dict:
    """
    Update campaign status. Only Admin/Manager.
    """
    require_role(user_email, ["admin", "manager"])
    
    result = update_row("campaigns", {"id": campaign_id}, {"status": new_status, "updated_at": datetime.now(timezone.utc).isoformat()})
    
    if result:
        log_activity(user_email, "update_status", "campaign", campaign_id, {"new_status": new_status})
        
    return result
