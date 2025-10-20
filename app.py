"""
======================================================
🤖 Gemini AI FastAPI Server (Updated)
Author: @Mr_Arman_08
Telegram Group: @Team_X_Og
======================================================
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os
import logging
from datetime import datetime

# Import new Google Gen AI SDK (replaces 'google.generativeai')
from google import genai

# ------------------------------------------------------
# ⚙️ Configuration
# ------------------------------------------------------
app = FastAPI(
    title="TeamXOg AI API",
    description="AI Response Generator using Google Gemini API (v2 SDK) | Owner: @Mr_Arman_08 | Telegram: @Team_X_Og",
    version="2.0.0"
)

# Logging setup
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure Gemini API key
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("❌ GOOGLE_API_KEY not found! Set it as an environment variable before running.")

client = genai.Client(api_key=API_KEY)

# ------------------------------------------------------
# 🧩 Root endpoint (info)
# ------------------------------------------------------
@app.get("/")
async def root():
    return JSONResponse({
        "status": "ok",
        "message": "Welcome to TeamXOg AI API 🤖",
        "usage": "Use /TeamXOg/Ai/Get/Response/getfast/query/?prompt=Your+text+here",
        "credits": {
            "Owner": "@Mr_Arman_08",
            "Telegram Group": "@Team_X_Og"
        }
    })

# ------------------------------------------------------
# ⚡ Main AI Endpoint
# ------------------------------------------------------
@app.get("/TeamXOg/Ai/Get/Response/getfast/query/")
async def get_fast_response(
    prompt: str = Query(..., description="User prompt for AI response"),
):
    start_time = datetime.utcnow()

    try:
        if not prompt.strip():
            return JSONResponse(
                {"success": False, "error": "Prompt cannot be empty."},
                status_code=400
            )

        # Use the Gemini 1.5 Flash model
        result = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        response_text = result.text if hasattr(result, "text") else "⚠️ No response generated."

        logging.info(f"✅ Prompt processed: '{prompt[:50]}'...")

        return JSONResponse({
            "success": True,
            "response": response_text,
            "model": "gemini-1.5-flash",
            "timestamp": str(start_time),
            "credits": {
                "Owner": "@Mr_Arman_08",
                "Telegram Group": "@Team_X_Og"
            }
        })

    except Exception as e:
        logging.error(f"❌ Error processing prompt: {str(e)}")
        return JSONResponse(
            {
                "success": False,
                "error": "Internal Server Error",
                "details": str(e),
                "credits": {
                    "Owner": "@Mr_Arman_08",
                    "Telegram Group": "@Team_X_Og"
                }
            },
            status_code=500
        )

# ------------------------------------------------------
# 🧠 Health Check Endpoint
# ------------------------------------------------------
@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "running",
        "service": "TeamXOg Gemini AI API",
        "timestamp": str(datetime.utcnow()),
        "credits": {
            "Owner": "@Mr_Arman_08",
            "Telegram Group": "@Team_X_Og"
        }
    })
