from utils.gemini import call_gemini 

# AGENT 3: Identify Gap in skills and suggest improvement areas

PROMPT = """
You are part of a resume reviewing application.

Your task is to analyze the candidate's technical skill profile and extract:

- skill_score: Rate the overall quality and completeness of the candidate's skills on a scale of 1–10.
- current_skills: Skills that are explicitly mentioned in the resume.
- missing_resume_skills: Important skills that are commonly expected for the candidate's career stage and primary domain but are not present in the resume.
- recommended_future_skills: Recommend skills that would strengthen the candidate's profile. For each recommendation include:
    - skill: Name of the skill
    - reason: Explain why learning this skill would improve the candidate's resume.
    - priority: High, Medium, or Low

Scoring Guidelines:

1–3:
Very limited technical skillset with major gaps for the candidate's career stage.

4–6:
Reasonable foundation but missing several important or commonly expected skills.

7–8:
Strong and relevant skillset with only a few notable gaps.

9–10:
Excellent, well-rounded, modern technical skillset that aligns very well with the candidate's experience and domain.

Guidelines:
- Base your analysis ONLY on information explicitly present in the resume.
- Never invent skills that are not mentioned.
- Missing skills should be reasonable suggestions for the candidate's career stage and domain.
- Prioritize practical, industry-relevant technologies.
- Be concise and avoid repeating recommendations.
- Return ONLY valid JSON matching the provided schema.
"""
RESPONSE_SCHEMA = {
    "type": "object",
    "properties":{
        "skill_score":{
            "type": "integer",
            "minimum": 1,
            "maximum": 10
        },
        "current_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_resume_skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "recommended_future_skills":{
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
    "required": ["skill_score","current_skills", "missing_resume_skills", "recommended_future_skills"]
}

def skill_gap_agent(context):
    return call_gemini(context, PROMPT, RESPONSE_SCHEMA)
