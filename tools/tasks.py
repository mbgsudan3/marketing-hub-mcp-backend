
from typing import Optional
from supabase_client import fetch_rows, insert_row, update_row
from tools.auth import require_role, get_user_role
from tools.activity import log_activity
from datetime import datetime, timezone


def list_tasks(assignee_email: Optional[str] = None, status: Optional[str] = None, user_email: Optional[str] = None) -> list[dict]:
    """
    Fetch tasks. 
    Team members can only see tasks assigned to them.
    Admin/Manager can see all.
    """
    filters = {}
    if status:
        filters["status"] = status
        
    # Role check logic for filtering
    if user_email:
        role = get_user_role(user_email)
        if role == "team":
            # Force filter by assignee if user is team
            # If they requested another assignee, they get nothing (or we override).
            # Let's override/enforce.
            filters["assignee"] = user_email
        elif assignee_email:
            filters["assignee"] = assignee_email
    elif assignee_email:
         filters["assignee"] = assignee_email
         
    return fetch_rows("tasks", filters)


def create_task(title: str, assignee_email: str, due_date: str, creator_email: str, related_campaign_id: Optional[str] = None) -> dict:
    """
    Create a new task. Admin/Manager only.
    """
    require_role(creator_email, ["admin", "manager"])
    
    data = {
        "title": title,
        "assignee": assignee_email,
        "due_date": due_date,
        "related_campaign_id": related_campaign_id,
        "status": "todo",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    result = insert_row("tasks", data)
    
    if result:
        log_activity(creator_email, "create_task", "task", result.get("id", "unknown"), {"title": title})
        
    return result


def update_task_status(task_id: str, new_status: str, user_email: str) -> dict:
    """
    Update task status. Admin/Manager only.
    """
    require_role(user_email, ["admin", "manager"])
    
    result = update_row("tasks", {"id": task_id}, {"status": new_status})
    
    if result:
        log_activity(user_email, "update_status", "task", task_id, {"new_status": new_status})
        
    return result
