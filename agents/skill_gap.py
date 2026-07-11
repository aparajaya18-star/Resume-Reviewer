from utils import client
import json
from google.genai import types 

PROMPT="""
You are part of a resume reviewing application.
Your task is to analyze the candidate's resume and extract:
- current_skills: skills you can identify in the current resume
- missing_skills: gaps in their current skills based on their domain, experience and other relevant information
- skill_suggestions: suggest skills best suited for elevating their resume and making their skill set seem more cohesive. Make sure to include:
    - skill: name of the skill
    - reason: why learning that skill would be helpful
    - priority: how important it is that you learn it

Guidelines: 
- Base your analysis ONLY on information explicitly present in the resume.
- Be concise and professional.
- Avoid repeating the same point.
- Focus on actionable feedback.
- Return ONLY valid JSON that matches the provided schema.
"""
RESPONSE_SCHEMA = {
    "type": "object",
    "properties":{
        "current_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "skill_suggestions":{
            "type": "array",
            "items": {
                "type": "object",
                "properties":
                {
                    "skill": {"type": "string"},
                    "reason": {"type": "string"},
                    "priority":{
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    }
                },
                "required": ["skill", "reason", "priority"]
            }
        }
    },
    "required": ["current_skills", "missing_skills", "skill_suggestions"]
}
# AGENT 2: Identify Gap in skills and suggest improvement areas
def skill_gap_agent(information):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=information,
        config=types.GenerateContentConfig(
            system_instruction=PROMPT,
            response_mime_type="application/json",
            response_json_schema=RESPONSE_SCHEMA,
            temperature=0.3
        )
    )

    return json.loads(response.text)