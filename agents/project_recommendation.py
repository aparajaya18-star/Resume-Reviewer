from utils.agent_call import call_gemini, search_web
from utils.builder import build_context

PLANNING_PROMPT = """
You are an AI career advisor helping generate search queries for project recommendations.

You are given:
- candidate profile
- current skill analysis
- resume strengths and weaknesses
- projects already completed

Your goal is to generate Google search queries that will find portfolio-worthy projects that best improve the candidate's resume.

Guidelines:

- Recommend projects appropriate for the candidate's experience level.
- Avoid suggesting projects very similar to projects already on the resume.
- Focus on projects that strengthen weak areas or showcase missing skills.
- Include a mix of practical portfolio projects and slightly ambitious stretch projects.
- Keep each search query concise and natural.
- Prefer queries likely to return GitHub repositories, tutorials, competitions, or implementation guides.
- Generate 3–5 diverse search queries. Each query should explore a different project direction. Together the queries should retrieve enough information to recommend 4–6 unique projects.
- The final recommendations should cover different categories whenever possible.

For example:
- cloud engineering
- backend systems
- machine learning
- data engineering
- web development
- automation
- open source contributions
- mobile
- DevOps

Each query should target a different project idea rather than a broad topic.

Good example:
- "streamlit llm dashboard github portfolio project"

Bad example:
- "AI projects"

Return ONLY a JSON array of strings.
"""

PLANNING_SCHEMA={
    "type": "array",
    "items": {
        "type": "string"
    }
}

PROJECT_SELECTION_PROMPT = """
You are an AI portfolio advisor.

You are given:

• Candidate profile
• Current skills
• Skills they should learn
• Existing portfolio projects
• Web search results

Your task is to recommend the best portfolio projects for THIS candidate.

Select only projects that:

- improve the resume
- develop missing skills
- are different from existing projects
- are realistic for the candidate's level
- have high portfolio value

When multiple search results describe the same project:

- merge them
- keep the best resources
- discard duplicates

Resource selection:

Prefer:

1. GitHub
2. Kaggle
3. Hugging Face
4. Official documentation
5. University resources

Avoid blogs unless no better source exists.

Rank candidate projects by:

1. Resume impact
2. Skill gap coverage
3. Originality
4. Technical depth
5. Availability of high-quality resources

Return only the highest-ranked projects.

For each recommendation:

- Give a concise descriptive title.
- Estimate difficulty realistically.
- List only the most important technical skills.
- Explain why this project is valuable specifically for this candidate.
- Keep the overview under 120 words.
- Provide at most three high-quality learning resources.
- Portfolio impact should reflect how much the project strengthens the resume.

Do not invent information that is unsupported by the search results.

Response Guidelines: 
- The JSON array must contain 4-6 objects.
- resources should contain 1–3 entries.
- skills should contain 3–8 technologies.
- Return ONLY valid JSON.
"""
PROJECT_SELECTION_SCHEMA={
    "type": "array",
    "items": {
        "type": "object",
        "properties":{
            "title": {"type": "string"},
            "difficulty": {
                "type": "string",
                "enum": ["Easy", "Medium", "High"]
            },
            "skills":
            {
                "type": "array",
                "items": {"type": "string"},
            },
            "why_now": {"type": "string"},
            "overview": {"type": "string"},
            "time_estimate": {
                "type": "string",
                "enum":[
                    "Weekend",
                    "1 week",
                    "2 weeks",
                    "1 month+"
                ]
            },
            "portfolio_impact": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10
            },
            "resources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "url": {"type": "string"}
                    },
                    "required": ["title", "url"]
                    }
                }
        },
        "required": ["title", "difficulty", "skills", "why_now", "overview", "time_estimate", "portfolio_impact", "resources"]
    }
}

def project_recommendation_agent(context):
    # --- Three Step Pipeline ---
    # Plan possible search queries for ideas
    project_context = build_context("project_planning", context)
    queries = call_gemini(project_context, PLANNING_PROMPT, PLANNING_SCHEMA)

    # Search the internet for relevant projects and resources
    raw_search =  search_web(queries)

    # Extract project information from search results
    choose_context = build_context("project_choose", context, raw_search)
    projects = call_gemini(choose_context, PROJECT_SELECTION_PROMPT,PROJECT_SELECTION_SCHEMA)

    return projects