import os
import asyncio
from fastmcp import FastMCP

# Import tools
import tools.auth as auth_tools
import tools.campaigns as campaigns_tools
import tools.tasks as tasks_tools
import tools.assets as assets_tools
import tools.activity as activity_tools
import tools.dashboard as dashboard_tools
import tools.notifications as notifications_tools
import tools.reports as reports_tools
import tools.automations as automations_tools
import tools.system as system_tools
import tools.ai_engine as ai_engine_tools
import scheduler

# Initialize FastMCP
mcp = FastMCP("Marketing Hub MCP")

# --- Tool Registration ---

# Auth
mcp.add_tool(auth_tools.get_user_by_email)
mcp.add_tool(auth_tools.get_user_role)
mcp.add_tool(auth_tools.list_team_members)

# Campaigns
mcp.add_tool(campaigns_tools.list_campaigns)
mcp.add_tool(campaigns_tools.create_campaign)
mcp.add_tool(campaigns_tools.update_campaign_status)

# Tasks
mcp.add_tool(tasks_tools.list_tasks)
mcp.add_tool(tasks_tools.create_task)
mcp.add_tool(tasks_tools.update_task_status)

# Assets
mcp.add_tool(assets_tools.list_assets)
mcp.add_tool(assets_tools.upload_asset)
mcp.add_tool(assets_tools.review_asset)

# Activity
mcp.add_tool(activity_tools.log_activity)
mcp.add_tool(activity_tools.list_activity)

# Dashboard
mcp.add_tool(dashboard_tools.marketing_snapshot)
mcp.add_tool(dashboard_tools.channel_performance)

# Notifications
mcp.add_tool(notifications_tools.send_whatsapp_message)
mcp.add_tool(notifications_tools.notify_campaign_status_change)
mcp.add_tool(notifications_tools.notify_overdue_tasks)
mcp.add_tool(notifications_tools.send_email_report)
mcp.add_tool(notifications_tools.send_campaign_update)
mcp.add_tool(notifications_tools.send_email)

# Reports
mcp.add_tool(reports_tools.generate_dashboard_summary)
mcp.add_tool(reports_tools.send_periodic_marketing_report)

# Automations
mcp.add_tool(automations_tools.list_automations)
mcp.add_tool(automations_tools.create_automation)
mcp.add_tool(automations_tools.toggle_automation)
mcp.add_tool(automations_tools.run_automation_trigger)

# System
mcp.add_tool(system_tools.check_backend_config)

# AI Engine
mcp.add_tool(ai_engine_tools.ai_campaign_review)
mcp.add_tool(ai_engine_tools.ai_generate_ideas)
mcp.add_tool(ai_engine_tools.ai_generate_copy)
mcp.add_tool(ai_engine_tools.ai_marketing_calendar)
mcp.add_tool(ai_engine_tools.ai_dev_assistant)


if __name__ == "__main__":
    print("Starting Marketing Hub Backend with FastMCP")
    # Start the scheduler in the background
    scheduler.start_scheduler()
    
    # Run user FastMCP on HTTP
    # Host is 0.0.0.0 for Docker/Railway
    # Port is injected by Railway via $PORT, defaulting to 8000
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
