import types
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Helper to define tool metadata
# Since we are manually registering, we need to define the Tool objects for list_tools

def tool_def(name, description, input_schema):
    return Tool(name=name, description=description, inputSchema=input_schema)

# Auth Tools Definitions
get_user_by_email_tool = tool_def(
    "get_user_by_email",
    "Get user details by email",
    {
        "type": "object",
        "properties": {"email": {"type": "string"}},
        "required": ["email"]
    }
)

get_user_role_tool = tool_def(
    "get_user_role",
    "Get the role of a user",
    {
        "type": "object",
        "properties": {"email": {"type": "string"}},
        "required": ["email"]
    }
)

list_team_members_tool = tool_def(
    "list_team_members",
    "List all team members",
    {"type": "object", "properties": {}}
)

# Campaigns Tools Definitions
list_campaigns_tool = tool_def(
    "list_campaigns",
    "List campaigns with optional filters",
    {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "owner_email": {"type": "string"}
        }
    }
)

create_campaign_tool = tool_def(
    "create_campaign",
    "Create a new campaign",
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "status": {"type": "string"},
            "owner_email": {"type": "string"}
        },
        "required": ["name", "owner_email"]
    }
)

update_campaign_status_tool = tool_def(
    "update_campaign_status",
    "Update the status of a campaign",
    {
        "type": "object",
        "properties": {
            "campaign_id": {"type": "string"},
            "new_status": {"type": "string"},
            "user_email": {"type": "string"}
        },
        "required": ["campaign_id", "new_status", "user_email"]
    }
)

# Tasks Tools Definitions
list_tasks_tool = tool_def(
    "list_tasks",
    "List tasks with optional filters",
    {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "assignee_email": {"type": "string"},
            "campaign_id": {"type": "string"}
        }
    }
)

create_task_tool = tool_def(
    "create_task",
    "Create a new task",
    {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "assignee_email": {"type": "string"},
            "due_date": {"type": "string"},
            "campaign_id": {"type": "string"},
            "creator_email": {"type": "string"}
        },
        "required": ["title", "creator_email"]
    }
)

update_task_status_tool = tool_def(
    "update_task_status",
    "Update the status of a task",
    {
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "new_status": {"type": "string"},
            "user_email": {"type": "string"}
        },
        "required": ["task_id", "new_status", "user_email"]
    }
)

# Assets Tools Definitions
list_assets_tool = tool_def(
    "list_assets",
    "List assets with optional filters",
    {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "campaign_id": {"type": "string"}
        }
    }
)

upload_asset_tool = tool_def(
    "upload_asset",
    "Upload a new asset (mock)",
    {
        "type": "object",
        "properties": {
            "file_url": {"type": "string"},
            "description": {"type": "string"},
            "campaign_id": {"type": "string"},
            "requester_email": {"type": "string"}
        },
        "required": ["file_url", "requester_email"]
    }
)

review_asset_tool = tool_def(
    "review_asset",
    "Review an asset (approve/reject)",
    {
        "type": "object",
        "properties": {
            "asset_id": {"type": "string"},
            "decision": {"type": "string", "enum": ["approved", "rejected"]},
            "reviewer_email": {"type": "string"}
        },
        "required": ["asset_id", "decision", "reviewer_email"]
    }
)

# Activity Tools Definitions
log_activity_tool = tool_def(
    "log_activity",
    "Log a system activity",
    {
        "type": "object",
        "properties": {
            "action": {"type": "string"},
            "entity_type": {"type": "string"},
            "entity_id": {"type": "string"},
            "actor_email": {"type": "string"},
            "metadata": {"type": "object"}
        },
        "required": ["action", "entity_type", "entity_id"]
    }
)

list_activity_tool = tool_def(
    "list_activity",
    "List recent activity logs",
    {
        "type": "object",
        "properties": {
            "limit": {"type": "integer"},
            "entity_type": {"type": "string"}
        }
    }
)

# Dashboard Tools Definitions
marketing_snapshot_tool = tool_def(
    "marketing_snapshot",
    "Get a snapshot of marketing KPIs",
    {"type": "object", "properties": {}}
)

channel_performance_tool = tool_def(
    "channel_performance",
    "Get channel performance metrics",
    {"type": "object", "properties": {}}
)
