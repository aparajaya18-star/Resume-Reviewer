import os
import json
from dotenv import load_dotenv
from google.genai import types 
from google import genai
from tavily import TavilyClient
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import streamlit as st

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

TEMPERATURES = {
    "parser": 0.1,
    "analysis": 0.2,
    "skills": 0.35,
    "ats": 0.15,
    "planning": 0.6,
    "selection": 0.25,
    "rewrite":0.35
}

# ---- Call Gemini api ----
def call_gemini(context, PROMPT, RESPONSE_SCHEMA, temp=0.3):
    response = gemini_client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=json.dumps(context, indent=2),
            config=types.GenerateContentConfig(
                system_instruction=PROMPT,
                response_mime_type="application/json",
                response_json_schema=RESPONSE_SCHEMA,
                temperature=temp
            )
        )
    return json.loads(response.text)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_search_results(query, n_results=5):
    local_results = []
    try:
        response = tavily_client.search(
                query=query,
                max_results=n_results,  
                topic="general",
                include_domains=[
                    "github.com", "kaggle.com", "huggingface.co", "learn.microsoft.com",
                    "developer.mozilla.org", "cloud.google.com", "aws.amazon.com",
                    "docs.docker.com", "fastapi.tiangolo.com", "docs.python.org",
                    "streamlit.io", "pytorch.org", "tensorflow.org", "scikit-learn.org",
                    "langchain.com", "roadmap.sh", "opencv.org", "react.dev"
                ]
            )
    
        for result in response["results"]: 
            local_results.append({  "query": query,
                                    "title": result["title"],
                                    "content": result["content"][:500],
                                    "url": result["url"],
                                    "domain": urlparse(result["url"]).netloc }
                                )
        return local_results
    except Exception as e:
        print(f"Search failed for '{query}': {e}")
        return []
    

def search_web(queries, n_results=5):
    worker = partial(fetch_search_results, n_results=n_results)

    with ThreadPoolExecutor(max_workers=min(5, len(queries))) as executor:
        return [
            result
            for query_results in executor.map(worker, queries)
            for result in query_results
        ]