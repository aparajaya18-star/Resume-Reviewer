import os
import json
from dotenv import load_dotenv
from google.genai import types 
from google import genai
from tavily import TavilyClient
from urllib.parse import urlparse

load_dotenv()

# -----Gemini API Key Configuration----
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# -----Tavily API Key Configuration----
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("Tavily API Key not provided. Please provide TAVILY_API_KEY as an environment variable")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# ---- Call Gemini api ----
def call_gemini(context, PROMPT, RESPONSE_SCHEMA):
    response = gemini_client.models.generate_content(
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

# ---- Use Gemini Google search tool -----
def search_web(queries, n_results=5):
    search_results = []
    for query in queries:
        response = tavily_client.search(
            query=query,
            max_results=n_results, # Default=5  
            topic="general",
            include_domains=[
                "github.com",
                "kaggle.com",
                "huggingface.co",
                "learn.microsoft.com",
                "developer.mozilla.org",
                "cloud.google.com",
                "aws.amazon.com",
                "docs.docker.com",
                "fastapi.tiangolo.com",
                "docs.python.org",
                "streamlit.io",
                "pytorch.org",
                "tensorflow.org",
                "scikit-learn.org",
                "langchain.com",
                "roadmap.sh",
                "opencv.org",
                "react.dev"
            ]
        )
        for result in response["results"]:
            search_results.append({
                "title": result["title"],
                "content": result["content"][:600],
                "url": result["url"],
                "domain": urlparse(result["url"]).netloc
            })
    return search_results