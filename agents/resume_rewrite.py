from utils.agent_call import call_gemini, TEMPERATURES
from utils.builder import build_context
from utils.timer import timed_step

PROMPT = """
ROLE

You are an expert technical resume writer and ATS optimization specialist.

OBJECTIVE

You are given:
- The candidate's original resume
- Structured information extracted from the resume
- Resume analysis
- ATS analysis
- Identified strengths
- Weaknesses
- Missing sections
- Formatting issues

Your task is to rewrite the resume to improve professionalism, readability and ATS compatibility while preserving every factual detail.

PRIMARY GOALS

- Improve clarity.
- Improve ATS compatibility.
- Improve formatting consistency.
- Improve wording.
- Preserve the candidate's original writing style whenever possible.
- Rewrite only sections that genuinely need improvement.
- If a section is already strong, return it unchanged.
- If a bullet point is already strong, copy it unchanged.

Example:

Good:
Developed a Flask web application that reduced document processing time by 40%.

Bad:
Worked on Flask.

NON-NEGOTIABLE RULES

1. Never invent experience.
2. Never invent projects.
3. Never invent technologies.
4. Never fabricate metrics or achievements.
5. Never change dates.
6. Never change chronology.
7. Never remove factual information.
8. Use stronger action verbs only when appropriate.
9. Remove redundant wording.
10. Make bullets concise.
11. Preserve section order unless changing it clearly improves readability or ATS compatibility.
12. If a section is reordered, explain why.
13. If something should exist but does not, mention it as a recommendation instead of inventing it.
14. Sort reported changes from most important to least important.

QUALITY CHECK

Before returning your answer verify:

- Every fact matches the original resume.
- No technologies were invented.
- No achievements were fabricated.
- No dates changed.
- Strong sections were preserved.
- JSON exactly follows the schema.

Formatting requirements:

The rewritten_resume.sections array should use these formats.

paragraphs:
content = [
    "Paragraph 1",
    "Paragraph 2"
]

bullets:
content = [
    "Bullet 1",
    "Bullet 2"
]

education:
content = [
    {
        "institution": "...",
        "degree": "...",
        "duration": "...",
        "details": [
            "...",
            "..."
        ]
    }
]

experience:
content = [
    {
        "role": "...",
        "company": "...",
        "duration": "...",
        "bullets": [
            "...",
            "...",
            "..."
        ]
    }
]

projects:
content = [
    {
        "name": "...",
        "tech_stack": [
            "Python",
            "Flask",
            "Streamlit"
        ],
        "bullets": [
            "...",
            "..."
        ]
    }
]

skills:
content = [
    {
        "category": "Languages",
        "items": [
            "Python",
            "C++"
        ]
    },
    {
        "category": "Frameworks",
        "items": [
            "Flask",
            "Streamlit"
        ]
    }
]

Return ONLY valid JSON.
"""
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "overview": {
            "type": "object",
            "properties": {
                "resume_quality": {"type": "string"},
                "summary": {"type": "string"},
                "major_changes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": [
                "resume_quality",
                "summary",
                "major_changes"
            ]
        },

        "rewritten_resume": {
            "type": "object",
            "properties": {

                "header": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "headline": {"type": "string"},
                        "location": {"type": "string"},
                        "phone": {"type": "string"},
                        "email": {"type": "string"},
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "url": {"type": "string"}
                                },
                                "required": ["label", "url"]
                            }
                        }
                    },
                    "required": [
                        "name",
                        "location",
                        "phone",
                        "email",
                        "links"
                    ]
                },

                "professional_summary": {
                    "type": "string"
                },

                "sections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {

                            "title": {
                                "type": "string"
                            },

                            "section_type": {
                                "type": "string",
                                "enum": [
                                    "bullets",
                                    "paragraphs",
                                    "education",
                                    "experience",
                                    "projects",
                                    "skills"
                                ]
                            },

                            "content": {"type": "array"}
                        },
                        "required": [
                            "title",
                            "section_type",
                            "content"
                        ]
                    }
                }
            },
            "required": [
                "header",
                "professional_summary",
                "sections"
            ]
        },

        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "section": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": [
                            "Minor",
                            "Moderate",
                            "Major"
                        ]
                    },
                    "change_type": {
                        "type": "string",
                        "enum": [
                            "ATS",
                            "Clarity",
                            "Formatting",
                            "Grammar",
                            "Wording"
                        ]
                    },
                    "original": {"type": "string"},
                    "improved": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "required": [
                    "section",
                    "severity",
                    "change_type",
                    "original",
                    "improved",
                    "reason"
                ]
            }
        },

        "additional_tips": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": [
                            "High",
                            "Medium",
                            "Low"
                        ]
                    },
                    "tip": {
                        "type": "string"
                    }
                },
                "required": [
                    "priority",
                    "tip"
                ]
            }
        }
    },
    "required": [
        "overview",
        "rewritten_resume",
        "changes",
        "additional_tips"
    ]
}

def rewrite_agent(context):
    rewrite_context = build_context("rewrite", context)
    return timed_step("Rewriting Resume", call_gemini, rewrite_context, PROMPT, RESPONSE_SCHEMA, temp=TEMPERATURES['rewrite']) 