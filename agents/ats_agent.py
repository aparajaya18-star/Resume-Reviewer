from utils.builder import build_context, build_query
from utils.agent_call import call_gemini, TEMPERATURES
from rag.database import retrieve, get_db

ats_database = get_db("ats")

PROMPT = """
You are an ATS (Applicant Tracking System) resume review agent.

You are given:
1. Structured information extracted from a resume.
2. Previous analysis from other agents.
3. Relevant ATS guidance retrieved from an ATS knowledge base.

Your job is to evaluate the resume with respect to:

1. Section completeness
2. Contact information and professional links
3. Formatting consistency
4. ATS readability
5. Keyword coverage
6. File metadata (if relevant)

Use the retrieved ATS guidance whenever it applies.

Do not recommend visual design changes that reduce ATS compatibility.

If the retrieved guidance does not mention a topic, rely only on the resume information.

Score ATS compatibility based only on factors affecting automated parsing and discoverability.
Do not reduce the score simply because the candidate has limited experience.

1–2
Poor ATS compatibility

3–4
Several major issues likely to hurt parsing

5–6
Generally readable but missing important ATS practices

7–8
Strong ATS compatibility with only minor improvements needed

9–10
Excellent ATS-ready resume

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
        "analysis":{
            "type": "string",
            "maxLength": 250
        },
        "issues":{
            "type": "array",
            "maxItems": 6,
            "items": {"type": "string"}
        },
        "improvements":{
            "type": "array",
            "maxItems": 6,
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
    response = call_gemini(resume_context, PROMPT, RESPONSE_SCHEMA, temp=TEMPERATURES['ats'])

    return {"retrieved_context": retrieved_info,
        **response}