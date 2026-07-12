from utils.builder import build_context
from agents.information_extraction import extract_information
from agents.resume_analysis import resume_analysis_agent
from agents.skill_gap import skill_gap_agent
from agents.ats_agent import ats_rag_agent

def run_pipeline(text, file_metadata, progress=None):
    # Create cumulative state to pass on inforamtion from agent to agent
    context = {
            "input": {
                "resume_text": text,
                "metadata": file_metadata,
            },
            "parsed": {},
            "analysis": {},
            "skills": {},
            "ats": {}
        }
    
    # AGENT 1
    if progress:
        progress("Extracting resume information...")
    context["parsed"] = extract_information(text)

    # AGENT 2
    if progress:
        progress("Analyzing resume...")
    context["analysis"] = resume_analysis_agent(
        build_context("analysis", context)
        )

    # AGENT 3
    if progress:
        progress("Finding skill gaps...")
    context["skills"]  = skill_gap_agent(
        build_context("skill", context)
    )

    # AGENT 4
    if progress:
        progress("Checking ATS compatibility...")
    context["ats"] = ats_rag_agent(context)

    return context