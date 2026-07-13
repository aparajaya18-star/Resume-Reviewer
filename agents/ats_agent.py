from utils.builder import build_context, build_query
from utils.agent_call import call_gemini
from rag.database import retrieve, get_db

ats_database = get_db("ats")

PROMPT = """
You are an ATS (Applicant Tracking System) resume review agent.

You are given:
1. Structured information extracted from a resume.
2. Previous analysis from other agents.
3. Relevant ATS guidance retrieved from an ATS knowledge base.

Your job is to evaluate the resume using BOTH the resume information and the retrieved ATS guidance.

Rules:
- Base recommendations on the retrieved ATS guidance whenever applicable.
- Do not invent ATS rules that are not supported by the retrieved documents.
- If the retrieved documents do not cover a topic, rely only on the resume information.
- Keep recommendations concise and actionable.
- Return only valid JSON matching the schema.
"""
RESPONSE_SCHEMA = {
    "type": "object",
    "properties":{
        "ats_score": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 10
                },
        "analysis":{"type": "string"},
        "issues":{
            "type": "array",
            "items": {"type": "string"}
        },
        "improvements":{
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["ats_score", "analysis", "issues", "improvements"]
}

def ats_rag_agent(context):

    query = build_query("ats", context)
    results = retrieve(query, ats_database)

    retrieved_info = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        retrieved_info.append(
            {
                "source": meta["source"],
                "section": meta.get("header2") or meta.get("header1"),
                "content": doc
            }
        )

    resume_context = build_context("ats", context, retrieved_info)
    response = call_gemini(resume_context, PROMPT, RESPONSE_SCHEMA)

    return {"retrieved_context": retrieved_info,
        **response}