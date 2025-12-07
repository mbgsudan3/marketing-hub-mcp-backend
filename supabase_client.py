import os
from typing import Optional, Union
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Mock Data Store
MOCK_DB = {
    "users": [
        {"email": "admin@example.com", "role": "admin", "name": "Admin User"},
        {"email": "manager@example.com", "role": "manager", "name": "Manager User"},
        {"email": "team@example.com", "role": "team", "name": "Team User"}
    ],
    "campaigns": [
        {"id": "1", "name": "Summer Sale", "status": "active", "channel": ["email", "social"], "start_date": "2024-06-01", "end_date": "2024-08-31", "owner_email": "manager@example.com"},
        {"id": "2", "name": "Black Friday", "status": "draft", "channel": ["ads"], "start_date": "2024-11-01", "end_date": "2024-11-30", "owner_email": "admin@example.com"}
    ],
    "tasks": [
        {"id": "1", "title": "Design Ad Creatives", "status": "in_progress", "assignee": "team@example.com", "due_date": "2024-06-15", "campaign_id": "1"},
        {"id": "2", "title": "Approve Budget", "status": "todo", "assignee": "manager@example.com", "due_date": "2024-06-10", "campaign_id": "1"}
    ],
    "assets": [
        {"id": "1", "description": "Banner Image", "file_url": "https://via.placeholder.com/300", "status": "pending", "requester_email": "team@example.com", "created_at": "2024-06-01T10:00:00Z"}
    ],
    "activity_log": [
        {"id": "1", "actor_email": "admin@example.com", "action": "login", "entity_type": "user", "entity_id": "admin@example.com", "created_at": "2024-06-01T09:00:00Z"}
    ]
}

def get_client() -> Optional[Client]:
    if os.environ.get("MOCK_MODE") == "true":
        return None
        
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ Supabase credentials missing -> Mock Mode Enabled")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"⚠️ Supabase connection failed ({e}) -> Mock Mode Enabled")
        return None

def fetch_rows(table: str, filters: Optional[dict] = None) -> list[dict]:
    """
    Fetch data from a Supabase table with optional filters.
    If Supabase client is not configured, operates in mock mode.
    """
    client = get_client()
    if not client:
        # Mock Mode
        data = MOCK_DB.get(table, [])
        if filters:
            return [row for row in data if all(row.get(k) == v for k, v in filters.items())]
        return data

    query = client.table(table).select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    response = query.execute()
    return response.data

def insert_row(table: str, data: dict) -> dict:
    """
    Insert data into a Supabase table.
    If Supabase client is not configured, operates in mock mode.
    """
    client = get_client()
    if not client:
        # Mock Mode
        if table not in MOCK_DB:
            MOCK_DB[table] = []
        # Generate a simple mock ID
        data["id"] = str(len(MOCK_DB[table]) + 1)
        MOCK_DB[table].append(data)
        return data

    response = client.table(table).insert(data).execute()
    if response.data:
        return response.data[0]
    return {}

def update_row(table: str, row_id: str, data: dict) -> dict:
    """
    Update a row in a Supabase table by ID.
    If Supabase client is not configured, operates in mock mode.
    """
    client = get_client()
    if not client:
        # Mock Mode
        rows = MOCK_DB.get(table, [])
        for row in rows:
            if row.get("id") == row_id:
                row.update(data)
                return row
        return {}

    response = client.table(table).update(data).eq("id", row_id).execute()
    if response.data:
        return response.data[0]
    return {}

def count_rows(table: str, filters: Optional[dict] = None) -> int:
    """
    Count rows in a Supabase table.
    If Supabase client is not configured, operates in mock mode.
    """
    client = get_client()
    if not client:
        # Mock Mode
        return len(fetch_rows(table, filters))

    query = client.table(table).select("*", count="exact")
    
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
            
    response = query.execute()
    return response.count if response.count is not None else 0
