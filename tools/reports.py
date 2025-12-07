from supabase_client import fetch_rows, count_rows
from tools.notifications import send_email_report

def generate_dashboard_summary(period: str = "daily") -> dict:
    """
    Generates a summary of key metrics for the dashboard.
    """
    # In a real app, we would filter by 'period' (created_at > now - 1 day, etc.)
    # For this MVP, we return total counts as a snapshot.
    
    summary = {
        "period": period,
        "active_campaigns": 0,
        "completed_campaigns": 0,
        "tasks_in_progress": 0,
        "overdue_tasks": 0,
        "pending_assets": 0
    }

    # Campaigns
    campaigns = fetch_rows("campaigns")
    for c in campaigns:
        if c.get("status") == "active":
            summary["active_campaigns"] += 1
        elif c.get("status") == "completed":
            summary["completed_campaigns"] += 1

    # Tasks
    tasks = fetch_rows("tasks")
    for t in tasks:
        if t.get("status") == "in_progress":
            summary["tasks_in_progress"] += 1
        # Mock overdue check
        if t.get("status") != "completed" and t.get("priority") == "high":
             summary["overdue_tasks"] += 1

    # Assets
    assets = fetch_rows("assets")
    for a in assets:
        if a.get("status") == "pending":
            summary["pending_assets"] += 1

    return summary

def send_periodic_marketing_report(to_email: str, period: str = "weekly") -> dict:
    """
    Generates and sends a marketing report via email.
    """
    summary = generate_dashboard_summary(period)
    
    subject = f"Marketing Hub - {period.capitalize()} Report"
    
    # Simple Text Body
    body_text = f"""
    Marketing Hub Report ({period})
    -----------------------------
    Active Campaigns: {summary['active_campaigns']}
    Completed Campaigns: {summary['completed_campaigns']}
    Tasks In Progress: {summary['tasks_in_progress']}
    Overdue Tasks: {summary['overdue_tasks']}
    Pending Assets: {summary['pending_assets']}
    
    Login to dashboard for more details.
    """
    
    # Simple HTML Body
    body_html = f"""
    <html>
    <body>
        <h2>Marketing Hub Report ({period})</h2>
        <ul>
            <li><strong>Active Campaigns:</strong> {summary['active_campaigns']}</li>
            <li><strong>Completed Campaigns:</strong> {summary['completed_campaigns']}</li>
            <li><strong>Tasks In Progress:</strong> {summary['tasks_in_progress']}</li>
            <li><strong>Overdue Tasks:</strong> {summary['overdue_tasks']}</li>
            <li><strong>Pending Assets:</strong> {summary['pending_assets']}</li>
        </ul>
        <p><a href="#">Login to dashboard</a> for more details.</p>
    </body>
    </html>
    """
    
    return send_email_report(to_email, subject, body_text, body_html)
