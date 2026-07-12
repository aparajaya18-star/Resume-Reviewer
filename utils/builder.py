def build_context(agent, context, retrieved_info = ""):
    match agent:
        case "analysis":
            return {
                "resume_text": context["input"]["resume_text"],
                "candidate": context["parsed"]["candidate_profile"],
                "metadata": context["input"]["metadata"]
            }
        case "skill":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "analysis": context["analysis"],
                "resume_text": context["input"]["resume_text"]
            }
        case "ats":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "analysis": context["analysis"],
                "skills": context["skills"],
                "metadata": context["input"]["metadata"],
                "retrieved_context": retrieved_info
            }
        
def build_query(agent, context):
    match agent:
        case "ats":
            return f"""
ATS best practices for a {context['parsed']['candidate_profile']['career_stage']} resume.

Missing Sections:
{context['analysis']['missing_sections']}

Formatting Issues:
{context['analysis']['formatting_issues']}

File Metadata:
{context["input"]["metadata"]}

How can this resume be improved for ATS parsing?
"""