import uuid
from datetime import datetime
from supabase_client import fetch_rows, insert_row, update_row
from tools.notifications import send_whatsapp_message, send_email_report
from tools.reports import send_periodic_marketing_report

# Mock storage for automations if table doesn't exist (for MVP resilience)
MOCK_AUTOMATIONS = [
    {
        "id": "1",
        "name": "Daily Overdue Task Alert",
        "is_enabled": True,
        "trigger_type": "task_overdue_daily",
        "condition_json": {"min_overdue": 1},
        "actions_json": [{"type": "whatsapp", "to": "manager"}],
        "created_at": datetime.now().isoformat()
    },
    {
        "id": "2",
        "name": "Weekly Email Report",
        "is_enabled": False,
        "trigger_type": "campaign_summary_weekly",
        "condition_json": {},
        "actions_json": [{"type": "email_report", "to": "admin@example.com"}],
        "created_at": datetime.now().isoformat()
    }
]

def list_automations() -> list:
    """
    Lists all configured automations.
    """
    try:
        rows = fetch_rows("automations")
        if not rows and not isinstance(rows, list): # Handle if fetch_rows returns None or error
             return MOCK_AUTOMATIONS
        return rows if rows else MOCK_AUTOMATIONS # Return mock if empty for demo
    except Exception:
        return MOCK_AUTOMATIONS

def create_automation(name: str, trigger_type: str, condition_json: dict, actions_json: list) -> dict:
    """
    Creates a new automation rule.
    """
    new_auto = {
        "id": str(uuid.uuid4()),
        "name": name,
        "is_enabled": True,
        "trigger_type": trigger_type,
        "condition_json": condition_json,
        "actions_json": actions_json,
        "created_at": datetime.now().isoformat()
    }
    
    try:
        result = insert_row("automations", new_auto)
        return result if result else new_auto
    except Exception as e:
        print(f"Failed to insert automation: {e}")
        # For MVP, just append to mock
        MOCK_AUTOMATIONS.append(new_auto)
        return new_auto

def toggle_automation(automation_id: str, enabled: bool) -> dict:
    """
    Enables or disables an automation.
    """
    try:
        result = update_row("automations", automation_id, {"is_enabled": enabled})
        return result
    except Exception:
        # Update mock
        for a in MOCK_AUTOMATIONS:
            if a["id"] == automation_id:
                a["is_enabled"] = enabled
                return a
        return {"error": "Automation not found"}

def run_automation_trigger(trigger_type: str) -> dict:
    """
    Executes all enabled automations for a specific trigger type.
    """
    automations = list_automations()
    executed = []
    
    for auto in automations:
        if auto.get("trigger_type") == trigger_type and auto.get("is_enabled"):
            # Evaluate condition (Mock logic)
            condition = auto.get("condition_json", {})
            should_run = True
            
            # Example condition logic
            if "min_overdue" in condition:
                # Check actual overdue tasks
                # tasks = fetch_rows("tasks") ...
                pass 
            
            if should_run:
                results = []
                for action in auto.get("actions_json", []):
                    action_type = action.get("type")
                    
                    if action_type == "whatsapp":
                        # Mock sending
                        res = send_whatsapp_message("mock_number", f"Automation Triggered: {auto['name']}")
                        results.append(res)
                    
                    elif action_type == "email_report":
                        to_email = action.get("to")
                        res = send_periodic_marketing_report(to_email, "weekly")
                        results.append(res)
                        
                executed.append({
                    "automation_id": auto["id"],
                    "name": auto["name"],
                    "results": results
                })
                
    return {"status": "success", "executed": executed}
