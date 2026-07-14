from utils.agent_call import call_gemini, TEMPERATURES

# AGENT 1: Extract basic Information from file (Common Use)

PROMPT = """
You are an information extraction agent for an AI-powered resume review system.

Your task is to extract structured information from a resume.

Extract ONLY information that is explicitly stated or can be directly inferred from the resume. Do NOT guess or fabricate any information.

Populate every field defined in the provided JSON schema.

Guidelines:

1. Candidate Profile
Extract:
- career_stage
    Choose one of:
    Student, Intern, Entry-level, Junior, Mid-level, Senior, Executive, Other
- primary_domain
    The candidate's primary technical domain or specialization.
    Examples:
    - Machine Learning
    - Data Science
    - Backend Development
    - Web Development
    - Cybersecurity
    - Robotics
- education_level
    Choose the highest completed or currently pursued education level:
    Middle School
    Secondary Education
    Undergraduate
    Postgraduate
    Doctoral
    Other
- years_of_experience
    Estimate total professional experience in years based only on internships, employment, research positions, or other explicitly stated experience.
    Do NOT count academic projects alone as work experience.

2. Education
Extract every education entry.
For each entry identify:
- degree
- institution
- year (if available)

3. Work Experience
Extract every internship, research role, freelance position, or full-time job.

For each position include:
- company
- role
- duration
- short summary of responsibilities or achievements

Preserve reverse chronological order whenever possible.

4. Skills
Extract only explicitly listed technical skills, programming languages, frameworks, tools, libraries, databases, cloud platforms, and technologies.

Do not infer missing skills.

5. Projects
Extract every significant project.

For each project include:
- name
- short description
- primary technologies or skills used

If technologies are not explicitly mentioned but are clearly stated in the project description, include them.

6. Certifications
Extract every certification exactly as written.

7. Major Achievements
Extract notable awards, rankings, publications, scholarships, leadership positions, competitions, or measurable accomplishments.

8. Links
Extract:
- GitHub links
- LinkedIn profile
- Portfolio or personal website
- Any remaining professional links under "other"

Rules:
- Return ONLY valid JSON matching the provided schema.
- Never invent information.
- If information is missing, return an empty array, empty object field, or empty string as appropriate.
- Do not include explanations, markdown, or additional text.
"""
RESPONSE_SCHEMA = {
    "type": "object",
    "properties":{
        "candidate_profile":{
            "type": "object",
            "properties":{
                "career_stage": {
                    "type": "string",
                    "enum":[
                        "Student",
                        "Intern",
                        "Entry-level",
                        "Junior",
                        "Mid-level",
                        "Senior",
                        "Executive",
                        "Other"
                    ]
                },
                "primary_domain": {"type": "string"},
                "education_level": {
                    "type": "string",
                    "enum": [
                        "Middle School",
                        "Secondary Education",
                        "Undergraduate",
                        "Postgraduate",
                        "Doctoral",
                        "Other"
                    ]},
                "years_of_experience": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 60
                }
            },
            "required": [
                "career_stage",
                "primary_domain",
                "years_of_experience",
                "education_level"
            ]
        },
        "education":{
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "degree": {"type": "string"},
                    "institution": {"type": "string"},
                    "year": {"type": "string"}
                },
                "required": ["degree", "institution"]
            }
        }, 
        "work_experience":{
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "role": {"type": "string"},
                    "duration": {"type": "string"},
                    "summary": {"type": "string"}
                },
                "required": ["company", "role", "duration"]
            }
        }, 
        "identified_skills":{
            "type": "array",
            "items": {"type": "string"}
        },
        "identified_projects":{
            "type": "array",
            "items": {
                "type": "object",
                "properties":{
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
                }
        }, 
        "certifications": {
            "type": "array",
            "items": {"type": "string"}
        },
        "major_achievements":{
            "type": "array",
            "items": {"type": "string"}
        },
        "links":{
            "type": "object",
            "properties": {
                "github": {
                    "type": "array",
                    "items": {"type": "string"}
                }, 
                "linkedin":  {"type": "string"},
                "portfolio": {"type": "string"},
                "other": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    },
    "required": ["candidate_profile",
                  "education",
                  "work_experience", 
                  "identified_skills", 
                  "identified_projects", 
                  "certifications",
                  "major_achievements",
                  "links"
                ]
}

def extract_information(text):
    return call_gemini(text, PROMPT, RESPONSE_SCHEMA, temp=TEMPERATURES['parser'])