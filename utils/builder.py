def build_context(agent, context, info = ""):
    match agent:
        case "analysis":
            return {
                "resume_text": context["input"]["resume_text"],
                "candidate": context["parsed"]["candidate_profile"],
                "education": context["parsed"]["education"],
                "work_experience": context["parsed"]["work_experience"],
                "projects": context["parsed"]["identified_projects"],
                "skills": context["parsed"]["identified_skills"],
                "achievements": context["parsed"]["major_achievements"],
                "certifications": context["parsed"]["certifications"],
                "links": context["parsed"]["links"]
            }
        case "skill":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "education": context["parsed"]["education"],
                "work_experience": context["parsed"]["work_experience"],
                "projects": context["parsed"]["identified_projects"],
                "certifications": context["parsed"]["certifications"],
                "current_skills": context["parsed"]["identified_skills"],
                "analysis": context["analysis"]
            }
        case "ats":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "experience_level": context["analysis"]["experience_level"],
                "skills": context["parsed"]["identified_skills"],
                "missing_sections": context['analysis']['missing_sections'],
                "formatting_issues": context['analysis']['formatting_issues'],
                "links": context["parsed"]["links"],
                "metadata": context["input"]["metadata"],
                "retrieved_context": info
            }
        case "project_planning":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "experience_level": context["analysis"]["experience_level"],
                "education": context["parsed"]["education"],
                "work_experience": context["parsed"]["work_experience"],
                "current_skills": context["parsed"]["identified_skills"],
                "target_skills": context["skills"]["recommended_skills"],
                "existing_projects": context["parsed"]["identified_projects"],
                "certifications": context["parsed"]["certifications"]
            }
        case "project_choose":
            return {
                "candidate": context["parsed"]["candidate_profile"],
                "experience_level": context["analysis"]["experience_level"],
                "education": context["parsed"]["education"],
                "work_experience": context["parsed"]["work_experience"],
                "current_skills": context["parsed"]["identified_skills"],
                "target_skills": context["skills"]["recommended_skills"],
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

Links:
Github: {context['parsed']['links']['github']}
LinkedIn: {context['parsed']['links']['linkedin']}
Potfolio: {context['parsed']['links']['portfolio']}
Others:
{context['parsed']['links']['other']}

How can this resume be improved for ATS parsing?
"""