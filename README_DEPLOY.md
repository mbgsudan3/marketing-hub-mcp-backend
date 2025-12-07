# Marketing Hub MCP Backend - Railway Deployment Guide

This guide explains how to deploy the Marketing Hub MCP backend to Railway.

## 1. Prerequisites

- A GitHub repository containing this `marketing-hub-mcp` folder.
- A Railway account (https://railway.app).
- A Supabase project (URL and Anon Key).

## 2. Repository Setup

Ensure your local folder contains the following structure (frontend files should be ignored or removed):

```
marketing-hub-mcp/
├── server.py
├── supabase_client.py
├── tools/
│   ├── __init__.py
│   ├── auth.py
│   ├── campaigns.py
│   ├── tasks.py
│   ├── assets.py
│   ├── activity.py
│   ├── dashboard.py
│   └── ...
├── requirements.txt
├── Procfile
└── README_DEPLOY.md
```

If you have a `web/` folder here, you should add it to `.gitignore` or remove it if it's already backed up elsewhere, to keep the backend deployment clean.

## 3. Deployment Steps

1.  **Push to GitHub**: Push your code to a GitHub repository.
2.  **New Project on Railway**:
    - Go to Railway Dashboard.
    - Click "New Project" -> "Deploy from GitHub repo".
    - Select your repository.
    - If this folder is the root of your repo, just deploy.
    - **Important**: If `marketing-hub-mcp` is a subfolder in your repo, go to "Settings" -> "Root Directory" in Railway and set it to `/marketing-hub-mcp`.

3.  **Configure Environment Variables**:
    - Go to the "Variables" tab in your Railway project.
    - Add the following variables:
        - `SUPABASE_URL`: Your Supabase Project URL.
        - `SUPABASE_KEY`: Your Supabase Anon Public Key (or Service Role Key if needed for admin tasks).

4.  **Wait for Build**: Railway will automatically detect `requirements.txt` and `Procfile`.
    - It will install dependencies: `pip install -r requirements.txt`.
    - It will start the app: `uvicorn server:app --host 0.0.0.0 --port 8000`.

## 4. Verification

Once deployed, Railway will provide a public URL (e.g., `https://marketing-hub-production.up.railway.app`).

- **Health Check**: Visit `https://<your-url>/health`. You should see `{"status": "ok"}`.
- **MCP Endpoint**: The endpoint `https://<your-url>/mcp` is now ready to verify your POST requests.

## 5. Connecting Frontend

Update your frontend `.env` (or Vercel environment variables) to point to this new backend:

```
VITE_MCP_URL=https://<your-url>/mcp
```
