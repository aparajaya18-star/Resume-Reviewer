import os
import json
from dotenv import load_dotenv
from google.genai import types 
from google import genai

load_dotenv()

# -----Gemini API Key Configuration----
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
client = genai.Client()

# ---- Call Gemini api ----
def call_gemini(context, PROMPT, RESPONSE_SCHEMA):
    response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=json.dumps(context, indent=2),
            config=types.GenerateContentConfig(
                system_instruction=PROMPT,
                response_mime_type="application/json",
                response_json_schema=RESPONSE_SCHEMA,
                temperature=0.3
            )
        )
    return json.loads(response.text)