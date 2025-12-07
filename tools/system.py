import os

def check_backend_config() -> dict:
    """
    Checks the backend configuration status (Supabase, WhatsApp, Email).
    """
    # Check Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    has_supabase = bool(supabase_url and supabase_key and "your-project" not in supabase_url)
    
    # Check WhatsApp (Twilio)
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
    has_whatsapp = bool(twilio_sid and twilio_token)
    
    # Check Email (SMTP)
    smtp_host = os.getenv("EMAIL_SMTP_HOST") or os.getenv("SMTP_HOST")
    has_email = bool(smtp_host)
    
    return {
        "mode": "supabase" if has_supabase else "mock",
        "has_supabase": has_supabase,
        "has_whatsapp": has_whatsapp,
        "has_email": has_email,
        "scheduler_enabled": os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"
    }
