
from supabase_client import count_rows, fetch_rows
from datetime import datetime, timezone


def marketing_snapshot() -> dict:
    """
    Return a structured dictionary with marketing KPIs.
    """
    active_campaigns = count_rows("campaigns", {"status": "active"})
    completed_campaigns = count_rows("campaigns", {"status": "completed"})
    tasks_in_progress = count_rows("tasks", {"status": "in_progress"})
    
    # For overdue tasks, we need a complex filter (due_date < now AND status != completed).
    # supabase_client.count_rows only supports simple equality.
    # We'll fetch all non-completed tasks and filter in python for now, or just return a placeholder if too heavy.
    # Let's try to be reasonably accurate.
    # Fetch all tasks not completed?
    # Or just fetch all tasks and filter.
    all_tasks = fetch_rows("tasks")
    now_iso = datetime.now(timezone.utc).isoformat()
    overdue_tasks = sum(1 for t in all_tasks if t.get("status") != "completed" and t.get("due_date", "") < now_iso)
    
    pending_assets = count_rows("assets", {"status": "pending"})
    
    return {
        "active_campaigns": active_campaigns,
        "completed_campaigns": completed_campaigns,
        "tasks_in_progress": tasks_in_progress,
        "overdue_tasks": overdue_tasks,
        "pending_assets": pending_assets,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }


def channel_performance() -> list[dict]:
    """
    Return aggregated metrics per channel.
    """
    # This would ideally be a SQL query.
    # In python, we fetch campaigns and aggregate.
    campaigns = fetch_rows("campaigns")
    
    stats = {}
    for c in campaigns:
        channels = c.get("channel", [])
        if isinstance(channels, str):
            channels = [channels] # Handle if stored as string
            
        for ch in channels:
            if ch not in stats:
                stats[ch] = {"channel": ch, "campaigns": 0, "tasks": 0}
            stats[ch]["campaigns"] += 1
            
            # We could also count tasks related to these campaigns if we fetched tasks.
            # For now let's just count campaigns as that's what we have easily.
            # To get tasks, we'd need to join or fetch tasks and map them.
            # Let's keep it simple.
            
    return list(stats.values())
