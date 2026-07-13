from utils.agent_call import call_gemini

# AGENT 1: Extract basic Information from file (Common Use)

PROMPT = """
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
RESPONSE_SCHEMA = {
    "type": "object",
    "properties":{
        "candidate_profile":{
            "type": "object",
            "properties":{
                "career_stage": {"type": "string"},
                "primary_domain": {"type": "string"},
                "years_of_experience": {"type": "number"},
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

def extract_information(text):
    return call_gemini(text, PROMPT, RESPONSE_SCHEMA)