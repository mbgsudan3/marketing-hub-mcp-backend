
from typing import Optional, Union
from supabase_client import fetch_rows


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Fetch a user by email from the 'users' table.
    """
    users = fetch_rows("users", {"email": email})
    if users:
        return users[0]
    return None


def get_user_role(email: str) -> str:
    """
    Get the role of a user by email. Returns 'unknown' if user not found.
    """
    user = get_user_by_email(email)
    if user:
        return user.get("role", "unknown")
    return "unknown"


def list_team_members() -> list[dict]:
    """
    List all users with their roles.
    """
    return fetch_rows("users")

def check_role(email: str, required_roles: Union[list[str], str]) -> bool:
    """
    Internal helper to check if a user has one of the required roles.
    
    Args:
        email: The email of the user.
        required_roles: A single role string or a list of allowed roles.
        
    Returns:
        True if the user has a required role, False otherwise.
    """
    role = get_user_role(email)
    if isinstance(required_roles, str):
        return role == required_roles
    return role in required_roles

def require_role(email: str, allowed_roles: list[str]):
    """
    Internal helper to enforce role checks. Raises ValueError if check fails.
    """
    if not check_role(email, allowed_roles):
        raise ValueError(f"User {email} does not have permission. Required: {allowed_roles}")
