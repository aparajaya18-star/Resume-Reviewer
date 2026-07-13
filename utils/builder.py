def build_context(agent, context, info = ""):
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
                "resume_text": context["input"]["resume_text"],
                "analysis": context["analysis"]
            }
        case "ats":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "resume_analysis": context["analysis"],
                "skills": context["skills"],
                "metadata": context["input"]["metadata"],
                "retrieved_context": info
            }
        case "project_planning":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "experience_level": context["analysis"]["experience_level"],
                "current_skills": context["skills"]["current_skills"],
                "target_skills": context["skills"]["recommended_future_skills"],
                "existing_projects": context["parsed"]["identified_projects"]
            }
        case "project_choose":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "experience_level": context["analysis"]["experience_level"],
                "current_skills": context["skills"]["current_skills"],
                "target_skills": context["skills"]["recommended_future_skills"],
                "existing_projects": context["parsed"]["identified_projects"],
                "search_results": info
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