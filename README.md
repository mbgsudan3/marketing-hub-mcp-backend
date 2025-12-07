# Marketing Hub MCP – Notifications & Automation Upgrade

This project has been upgraded with advanced features for notifications, reporting, and automation.

## New Features
- **WhatsApp Integration**: Send alerts via Twilio.
- **Email Reporting**: Send HTML reports via SMTP.
- **Automation Scheduler**: Background jobs for daily digests and weekly reports (APScheduler).
- **System Health Check**: Dashboard banner showing backend mode (Supabase vs Mock).
- **Settings Page**: Configure notification preferences and view system status.

## Configuration
Add these to your `.env` file:

```env
# Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# SMTP (Email)
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=your_email
EMAIL_SMTP_PASSWORD=your_password
EMAIL_FROM_ADDRESS=marketing@example.com

# Scheduler
ENABLE_SCHEDULER=true

# AI Engine (Optional)
OPENAI_API_KEY=sk-...
```

## AI Assistant (MIE)
The **Marketing Intelligence Engine** provides AI-powered insights:
- **Campaign Review**: Scores campaigns and suggests improvements.
- **Creative Ideas**: Generates marketing concepts.
- **Copywriting**: Writes copy in various styles.
- **Calendar**: Auto-generates marketing schedules.
- **Dev Assistant**: Answers questions about the project codebase.

If `OPENAI_API_KEY` is missing, the AI tools return **mock data** for demonstration purposes.

## Mock Mode
If credentials are missing, the system gracefully falls back to **Mock Mode**:
- **Backend**: Returns mock data for tools.
- **Frontend**: Displays a yellow banner.
- **Notifications**: Logs "Simulated send" instead of failing.

---

# Marketing Hub MCP

A FastMCP server for marketing operations, integrated with Supabase.

## Setup

1.  **Install Dependencies**:
    Ensure you have `fastmcp` and `supabase` installed.
    ```bash
    pip install fastmcp supabase python-dotenv
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your Supabase credentials.
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```

## Running the Server

### Development (STDIO)
Run the server directly with Python. This uses the STDIO transport by default, which is suitable for testing with MCP clients like Claude Desktop or other MCP-compatible tools.

```bash
python server.py
```

### HTTP Mode
To run in HTTP mode (if enabled in `server.py`), you can modify the run command in `server.py` or use the FastMCP CLI if applicable.
Currently, `server.py` is configured to run in STDIO mode by default.

## Tools

The server provides the following tools:

-   **Campaigns**: `list_campaigns`, `create_campaign`
-   **Tasks**: `list_tasks`, `create_task`
-   **Assets**: `fetch_assets`, `upload_asset`, `review_asset`
-   **Activity**: `log_activity`
-   **Dashboard**: `marketing_snapshot`

## Supabase Configuration

Ensure your Supabase project has the following tables:
-   `campaigns`
-   `tasks`
-   `assets`
-   `activity_log`

## Example Usage

**List Campaigns:**
```json
{
  "name": "list_campaigns",
  "arguments": {
    "status": "active"
  }
}
```
