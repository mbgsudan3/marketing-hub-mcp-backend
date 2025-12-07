import os
import json
import requests
import glob
from datetime import datetime, timedelta

def _call_openai(system_prompt: str, user_prompt: str) -> str:
    """
    Helper to call OpenAI API. Returns None if call fails or no key.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o", # or gpt-3.5-turbo
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"OpenAI API Error: {response.text}")
            return None
    except Exception as e:
        print(f"OpenAI Call Failed: {e}")
        return None

def ai_campaign_review(campaign: dict) -> dict:
    """
    Analyzes a campaign and provides insights.
    """
    prompt = f"Analyze this marketing campaign: {json.dumps(campaign)}. Provide a score (0-100), strengths, weaknesses, recommendations, and a predicted trend (improving, stable, declining). Return JSON."
    
    ai_response = _call_openai("You are a senior marketing strategist.", prompt)
    
    if ai_response:
        try:
            # Attempt to parse JSON from AI (cleanup markdown if needed)
            clean_json = ai_response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            pass # Fallback to mock if parsing fails

    # Mock Fallback
    return {
        "score": 78,
        "strengths": ["Strong visual identity", "Clear call-to-action", "Good initial engagement"],
        "weaknesses": ["Target audience too broad", "Budget allocation unclear"],
        "recommendations": [
            "Narrow down the target demographic to 25-34yo.",
            "Increase spend on Instagram Reels.",
            "A/B test the headline copy."
        ],
        "predicted_trend": "stable",
        "source": "mock"
    }

def ai_generate_ideas(topic: str, count: int = 5) -> list:
    """
    Generates creative marketing ideas for a topic.
    """
    prompt = f"Generate {count} creative marketing ideas for: {topic}. Return a JSON list of strings."
    
    ai_response = _call_openai("You are a creative director.", prompt)
    
    if ai_response:
        try:
            clean_json = ai_response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            pass

    # Mock Fallback
    return [
        f"Viral TikTok challenge about {topic}",
        f"Interactive webinar series featuring experts on {topic}",
        f"User-generated content contest with {topic} theme",
        f"Partnership with micro-influencers in the {topic} niche",
        f"Gamified loyalty program rewards for {topic}"
    ]

def ai_generate_copy(style: str, details: dict) -> str:
    """
    Generates marketing copy based on style and details.
    """
    prompt = f"Write marketing copy. Style: {style}. Details: {json.dumps(details)}."
    
    ai_response = _call_openai("You are an expert copywriter.", prompt)
    
    if ai_response:
        return ai_response

    # Mock Fallback
    return f"[{style.upper()} COPY]\n\nUnlock the full potential of your business with our latest offering. We've listened to your feedback and crafted a solution that perfectly matches your needs.\n\nKey Benefit: {details.get('benefit', 'Efficiency')}\nCall to Action: {details.get('cta', 'Sign Up Now')}\n\nDon't miss out!"

def ai_marketing_calendar(start_date: str, weeks: int = 4) -> list:
    """
    Generates a marketing calendar.
    """
    prompt = f"Generate a {weeks}-week marketing calendar starting {start_date}. Return JSON list of objects with 'date', 'channel', 'activity', 'topic'."
    
    ai_response = _call_openai("You are a marketing planner.", prompt)
    
    if ai_response:
        try:
            clean_json = ai_response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except:
            pass

    # Mock Fallback
    calendar = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    channels = ["Email", "Social Media", "Blog", "Ads"]
    activities = ["Post", "Blast", "Publish", "Launch"]
    
    for i in range(weeks * 3): # ~3 activities per week
        day_offset = (i * 2) + 1
        date = (start + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        calendar.append({
            "date": date,
            "channel": channels[i % len(channels)],
            "activity": activities[i % len(activities)],
            "topic": f"Week {i//3 + 1} Focus Topic"
        })
    
    return calendar

def ai_dev_assistant(question: str) -> dict:
    """
    Developer assistant that can read local files to answer questions.
    """
    # Simple file context gathering (safe subset)
    context = ""
    try:
        # Read server.py and tools/*.py to give context
        files_to_read = ["server.py"] + glob.glob("tools/*.py")
        for fpath in files_to_read:
            if os.path.exists(fpath):
                with open(fpath, "r") as f:
                    content = f.read()
                    # Truncate large files for context window safety if using real API
                    context += f"\n--- File: {fpath} ---\n{content[:2000]}\n"
    except Exception as e:
        context = f"Error reading files: {e}"

    prompt = f"Question: {question}\n\nContext from project files:\n{context}"
    
    ai_response = _call_openai("You are a senior python developer assisting with this specific project.", prompt)
    
    if ai_response:
        return {
            "answer": ai_response,
            "files_analyzed": files_to_read
        }

    # Mock Fallback
    return {
        "answer": f"I analyzed the project structure. Based on your question '{question}', here is a suggestion:\n\nIf you are asking about the backend, check 'server.py' for route definitions. For new tools, look into the 'tools/' directory.\n\n(This is a mock response. Configure OPENAI_API_KEY for real code analysis.)",
        "files_analyzed": ["server.py", "tools/*.py"],
        "source": "mock"
    }
