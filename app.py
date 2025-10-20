"""
======================================================
🤖 Gemini AI FastAPI Server (Enhanced)
Author: @Mr_Arman_08
Telegram Group: @Team_X_Og
======================================================
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os
import logging
from datetime import datetime
from typing import List

# Import new Google Gen AI SDK
from google import genai

# ------------------------------------------------------
# ⚙️ Configuration
# ------------------------------------------------------
app = FastAPI(
    title="TeamXOg AI API",
    description="AI Response Generator using Google Gemini API (v2 SDK) | Owner: @Mr_Arman_08 | Telegram: @Team_X_Og",
    version="2.1.0"
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
        "usage": "Use GET /TeamXOg/Ai/Get/Response/getfast/query/?prompt=Your+text+here",
        "credits": {
            "Owner": "@Mr_Arman_08",
            "Telegram Group": "@Team_X_Og"
        },
        "timestamp_utc": datetime.utcnow().isoformat()
    })

# ------------------------------------------------------
# 📜 List available models endpoint
# ------------------------------------------------------
@app.get("/TeamXOg/Ai/Models")
async def list_models() -> JSONResponse:
    try:
        models = client.models.list()
        supported_models = [
            {"name": m.name, "description": m.description or "No description", "supported_actions": m.supported_actions}
            for m in models
            if "generateContent" in m.supported_actions
        ]

        return JSONResponse({
            "success": True,
            "available_models": supported_models,
            "count": len(supported_models),
            "timestamp_utc": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logging.error(f"❌ Failed to fetch models list: {e}")
        return JSONResponse({
            "success": False,
            "error": "Failed to fetch models list",
            "details": str(e),
            "timestamp_utc": datetime.utcnow().isoformat()
        }, status_code=500)

# ------------------------------------------------------
# ⚡ Main AI Endpoint
# ------------------------------------------------------
@app.get("/TeamXOg/Ai/Get/Response/getfast/query/")
async def get_fast_response(
    prompt: str = Query(..., description="User prompt for AI response"),
):
    start_time = datetime.utcnow()

    try:
        prompt_clean = prompt.strip()
        if not prompt_clean:
            return JSONResponse(
                {"success": False, "error": "Prompt cannot be empty."},
                status_code=400
            )

        model_name = "gemini-2.5-flash"
        result = client.models.generate_content(
            model=model_name,
            contents=prompt_clean
        )

        response_text = result.text if hasattr(result, "text") else "⚠️ No response generated."

        # Compute request processing time in ms
        duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        logging.info(f"✅ Prompt processed: '{prompt_clean[:50]}'... | Model: {model_name}")

        # Clean, friendly response
        return JSONResponse({
            "success": True,
            "model_used": model_name,
            "timestamp_utc": start_time.isoformat(),
            "duration_ms": duration_ms,
            "prompt_preview": prompt_clean[:100] + ("..." if len(prompt_clean) > 100 else ""),
            "response": response_text,
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
                "timestamp_utc": datetime.utcnow().isoformat(),
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
        "timestamp_utc": datetime.utcnow().isoformat(),
        "credits": {
            "Owner": "@Mr_Arman_08",
            "Telegram Group": "@Team_X_Og"
        }
    })
