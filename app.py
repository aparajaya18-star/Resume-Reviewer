import streamlit as st

from utils import load_pdf, extract_information
from agents.resume_analysis import resume_analysis_agent
from agents.skill_gap import skill_gap_agent

# ----- Sreamlit app -----

# Configure Streamlit app
st.set_page_config(
    page_title="Resume Reviewer",
    layout="wide"
)

st.title("Resume Reviewer")
#st.caption("") -> add later

st.header("Resume Upload")
uploaded_file = st.file_uploader("Upload files", type="pdf")

submit_button = st.button("Submit for review")

if uploaded_file and submit_button:
    context = {}
    with st.spinner("Reviewing documents..."):
        # Load text from File
        text, num_pages  = load_pdf(uploaded_file)
        if not text.strip():
            st.error("No text could be extracted from this PDF.")
            st.stop()

        # Save File Metadata
        file_metadata = {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size,
            "total pages": num_pages
        }

        # Extract Basic information from File
        file_basic_info = extract_information(text)

        # Create cumulative state to pass on inforamtion from agent to agent
        context = {
            "resume_text": text,
            "metadata": file_metadata,
            "parsed": file_basic_info,
            "analysis": {},
            "skills": {}
        }

        # Get objective analysis of file [AGENT 1]
        try:
            context["analysis"] = resume_analysis_agent(context)
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()
        
        # Get objective analysis of file [AGENT 1]
        try:
           context["skills"]  = skill_gap_agent(context)
        except Exception as e:
            st.error(f"Skill Gap Analysis failed: {e}")
            st.stop()

    # ---- Resume Analysis -----
    st.divider()
    st.header("Overview")  

    col1, col2 = st.columns(2)
    with col1:
        st.success("Strengths")
        for s in context["analysis"]["strengths"]:
            st.write(f"• {s}")

    with col2:
        st.warning("Weaknesses")
        for w in context["analysis"]["weaknesses"]:
            st.write(f"• {w}")

    st.subheader("Experience Level: ")
    st.write(f"{context["analysis"]['experience_level']}/10")

    if context["analysis"].get("missing_sections"):
        st.subheader("Missing Sections:")
        for m in context["analysis"]["missing_sections"]:
            st.write(f"• {m}")

    if context["analysis"].get("formatting_issues"):
        st.subheader("Formatting Issues:")
        for i in context["analysis"]["formatting_issues"]:
            st.write(f"• {i}")

    st.subheader("ATS Friendliness:")
    st.write(f"Score: {context["analysis"]['ats_friendliness']['rating']}/10")
    st.write(f"Summary: {context["analysis"]['ats_friendliness']['summary']}")

    # ---- Skill Gap -----
    st.divider()
    st.header("Skills Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.success("Current Skills")
        for s in context["skills"]["current_skills"]:
            st.write(f"• {s}")

    with col2:
        st.warning("Missing Skills")
        for w in context["skills"]["missing_skills"]:
            st.write(f"• {w}")

    st.subheader("Suggested Skills")
    for suggestion in context["skills"]["skill_suggestions"]:
        st.write("Skill: ", suggestion['skill'])
        st.write(f"Reason: {suggestion['reason']}")
        st.write(f"Priority: ",suggestion['priority'])