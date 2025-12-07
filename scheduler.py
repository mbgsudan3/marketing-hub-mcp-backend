import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from tools.notifications import send_email, send_whatsapp_message
from tools.reports import generate_dashboard_summary
from supabase_client import fetch_rows

# Configure logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.WARNING)

def job_daily_task_digest():
    """
    Runs daily to send task digests to users.
    """
    print("Running job: daily_task_digest")
    # Mock logic: Fetch all tasks, group by assignee, send email
    tasks = fetch_rows("tasks")
    if not tasks:
        return

    tasks_by_user = {}
    for t in tasks:
        assignee = t.get("assignee_email")
        if assignee:
            if assignee not in tasks_by_user:
                tasks_by_user[assignee] = []
            tasks_by_user[assignee].append(t)
            
    for email, user_tasks in tasks_by_user.items():
        count = len(user_tasks)
        subject = f"Daily Task Digest: {count} tasks assigned to you"
        html = f"<h3>You have {count} tasks:</h3><ul>"
        for t in user_tasks:
            html += f"<li>{t.get('title')} ({t.get('status')})</li>"
        html += "</ul>"
        
        send_email(email, subject, html)

def job_weekly_campaign_report():
    """
    Runs weekly to send campaign report to admin.
    """
    print("Running job: weekly_campaign_report")
    summary = generate_dashboard_summary("weekly")
    
    # Send to admin (mock email)
    admin_email = "admin@example.com"
    subject = "Weekly Campaign Report"
    html = f"""
    <h2>Weekly Report</h2>
    <p>Active Campaigns: {summary['active_campaigns']}</p>
    <p>Completed Campaigns: {summary['completed_campaigns']}</p>
    """
    send_email(admin_email, subject, html)

def job_archive_finished_campaigns():
    """
    Runs hourly to archive finished campaigns.
    """
    print("Running job: archive_finished_campaigns")
    # Mock logic: find campaigns with end_date < now
    pass

def start_scheduler():
    """
    Starts the background scheduler.
    """
    if os.getenv("ENABLE_SCHEDULER", "false").lower() != "true":
        print("Scheduler disabled (ENABLE_SCHEDULER != true)")
        return

    scheduler = BackgroundScheduler()
    
    # Daily at 09:00
    scheduler.add_job(job_daily_task_digest, CronTrigger(hour=9, minute=0))
    
    # Weekly on Friday at 17:00
    scheduler.add_job(job_weekly_campaign_report, CronTrigger(day_of_week='fri', hour=17, minute=0))
    
    # Hourly
    scheduler.add_job(job_archive_finished_campaigns, CronTrigger(minute=0))
    
    scheduler.start()
    print("Scheduler started.")
