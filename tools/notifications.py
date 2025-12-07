import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from supabase_client import get_client, fetch_rows

def send_whatsapp_message(to_number: str, message_body: str) -> dict:
    """
    Sends a WhatsApp message using Twilio.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")

    if not all([account_sid, auth_token, from_number]):
        return {"status": "mock", "message": "WhatsApp send simulated (missing credentials)", "provider": "twilio"}

    try:
        # Twilio API URL
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        # Twilio expects form-encoded data
        data = {
            "From": from_number,
            "To": f"whatsapp:{to_number}",
            "Body": message_body
        }
        
        response = requests.post(url, data=data, auth=(account_sid, auth_token), timeout=10)
        
        if response.status_code >= 200 and response.status_code < 300:
            res_json = response.json()
            return {"status": "success", "sid": res_json.get("sid"), "to": to_number, "provider": "twilio"}
        else:
            return {"status": "error", "message": response.text, "provider": "twilio"}
            
    except Exception as e:
        print(f"WhatsApp send error: {e}")
        return {"status": "error", "message": str(e), "provider": "twilio"}

def send_campaign_update(campaign_id: str, to_number: str) -> dict:
    """
    Sends a campaign status update via WhatsApp.
    """
    campaigns = fetch_rows("campaigns", {"id": campaign_id})
    if not campaigns:
        return {"status": "error", "message": "Campaign not found"}
    
    campaign = campaigns[0]
    message = f"📢 Update: Campaign '{campaign.get('name')}' is currently {campaign.get('status', 'unknown').upper()}."
    
    return send_whatsapp_message(to_number, message)

# Alias for backward compatibility if needed, or just use the new one
def notify_campaign_status_change(campaign_id: str, new_status: str) -> dict:
    # Re-implement using the new helper if we want, or keep existing logic.
    # The prompt asked for `send_campaign_update`.
    # Let's keep this one but make it use the new `send_whatsapp_message` internally if it resolves a number.
    # For now, I'll leave the previous implementation but update it to use the new `send_whatsapp_message` signature if needed.
    # Actually, let's just update this to use the new `send_whatsapp_message` logic.
    
    campaigns = fetch_rows("campaigns", {"id": campaign_id})
    if not campaigns:
        return {"status": "error", "message": "Campaign not found"}
    
    campaign = campaigns[0]
    owner_email = campaign.get("owner_email")
    
    if not owner_email:
        return {"status": "skipped", "reason": "no_owner_email"}

    users = fetch_rows("users", {"email": owner_email})
    if not users:
        return {"status": "skipped", "reason": "owner_not_found"}
    
    phone_number = users[0].get("phone_number")
    if not phone_number:
        return {"status": "skipped", "reason": "no_phone_number"}

    message = f"📢 Campaign Update: '{campaign.get('name')}' is now {new_status.upper()}."
    return send_whatsapp_message(phone_number, message)

def notify_overdue_tasks(manager_email: str) -> dict:
    users = fetch_rows("users", {"email": manager_email})
    if not users:
        return {"status": "error", "message": "Manager not found"}
    
    phone_number = users[0].get("phone_number")
    if not phone_number:
        return {"status": "skipped", "reason": "no_phone_number"}

    # Mock overdue check
    all_tasks = fetch_rows("tasks")
    overdue_count = 0
    for t in all_tasks:
        if t.get("status") != "completed": 
             overdue_count += 1

    if overdue_count == 0:
        return {"status": "skipped", "reason": "no_overdue_tasks"}

    message = f"⚠️ Alert: You have {overdue_count} tasks requiring attention."
    return send_whatsapp_message(phone_number, message)

def send_email(to_email: str, subject: str, html_body: str) -> dict:
    """
    Sends an email using SMTP.
    """
    smtp_host = os.getenv("EMAIL_SMTP_HOST") or os.getenv("SMTP_HOST")
    smtp_port = os.getenv("EMAIL_SMTP_PORT") or os.getenv("SMTP_PORT")
    smtp_user = os.getenv("EMAIL_SMTP_USER") or os.getenv("SMTP_USER")
    smtp_password = os.getenv("EMAIL_SMTP_PASSWORD") or os.getenv("SMTP_PASSWORD")
    from_addr = os.getenv("EMAIL_FROM_ADDRESS") or os.getenv("EMAIL_FROM")

    if not all([smtp_host, smtp_port, smtp_user, smtp_password, from_addr]):
        return {"status": "mock", "message": "Email send simulated (missing credentials)", "provider": "email"}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_email

        part = MIMEText(html_body, "html")
        msg.attach(part)

        server = smtplib.SMTP(smtp_host, int(smtp_port))
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_addr, to_email, msg.as_string())
        server.quit()

        return {"status": "success", "provider": "email"}
    except Exception as e:
        print(f"Email send error: {e}")
        return {"status": "error", "message": str(e), "provider": "email"}

# Alias for backward compatibility/consistency
def send_email_report(to_email: str, subject: str, body_text: str, body_html: str = None) -> dict:
    return send_email(to_email, subject, body_html or body_text)
