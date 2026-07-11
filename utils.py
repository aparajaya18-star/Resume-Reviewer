import os
import pymupdf
from google import genai

import json
from google.genai import types 
from dotenv import load_dotenv

load_dotenv()

# -----Gemini API Key Configuration----
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
client = genai.Client()

# ----Extract text from pdf (Common Use)-----
def load_pdf(uploaded_file):
    text = []
    pages = 0

    # Read the file buffers from Streamlit
    file_bytes = uploaded_file.read()

    # Open the pdf from memory stream
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        # Iterate through each pdf page
        for page in doc:
            pages += 1
            # Extract text blocks, sorted by natural reading order (helps seperate different paragraphs and headings)
            blocks = page.get_text("blocks", sort=True)
            for block in blocks:
                # Block[4] contains extracted text string
                text.append(block[4])

    full_text = "\n\n".join(text)
    return full_text, pages

# ----Extract basic Information from file (Common Use)-----
def extract_information(text):
    prompt = """
You are an information parser for a resume reviewing application.

Analyze the resume text and extract any structured candidate information.

You have to identify:
* candidate_profile
    - career_stage (eg Student, Intern, long term employee etc)
    - primary_domain (eg Machine Learning, Robotics, Architectural Design)
    - years_of_experience (eg 0, 1, 2, 3.5)
    - education_level (eg B.Tech, M.S, PhD)
* identified_skills (eg Python, Flask, TensorFlow, SQL, Leadership)
* identified_projects (eg Fake News Detection, RAG Chatbot)
* major_achievements (eg Hackathon Winner, Fundraised Rs.25,000 etc)

Rules:
- Return ONLY valid JSON matching the provided schema.
- Do not invent missing information.
- Do not include explanations.
"""
    response_schema = {
        "type": "object",
        "properties":{
            "candidate_profile":{
                "type": "object",
                "properties":{
                    "career_stage": {"type": "string"},
                    "primary_domain": {"type": "string"},
                    "years_of_experience": {"type": "integer"},
                    "education_level": {"type": "string"}
                },
                "required": [
                    "career_stage",
                    "primary_domain",
                    "years_of_experience",
                    "education_level"
                ]
            },
            "identified_skills":{
                "type": "array",
                "items": {"type": ["string", "null"]}
            },
            "identified_projects":{
                "type": "array",
                "items": {"type": ["string", "null"] }
            },
            "major_achievements":{
                "type": "array",
                "items": {"type": ["string", "null"]}
            }
        },
        "required": ["candidate_profile", "identified_skills", "identified_projects", "major_achievements"]
    }
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=text,
        config=types.GenerateContentConfig(
            system_instruction=prompt,
            response_mime_type="application/json",
            response_json_schema=response_schema,
            temperature=0.3
        )
    )

    return json.loads(response.text)