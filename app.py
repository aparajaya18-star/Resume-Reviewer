import streamlit as st

from utils.pdf import load_pdf
from orchestrator import run_pipeline

# ----- Sreamlit app -----

# Configure Streamlit app
st.set_page_config(
    page_title="Resume Reviewer",
    layout="centered"
)
#st.caption("") -> add later

left, center, right = st.columns([1,16,1])

with center:
    #st.title("Resume Reviewer")
    st.markdown("<h1 style='text-align: center;'>Resume Reviewer</h1>", unsafe_allow_html=True)
    with st.container(border=True):

        st.subheader("📄 Upload Resume")

        st.caption(
            "Upload a PDF resume to receive AI-powered feedback."
        )

        uploaded_file = st.file_uploader(
            "",
            type="pdf",
            label_visibility="collapsed"
        )

        submit_button = st.button(
            "Analyze Resume",
            use_container_width=True
        )

if uploaded_file and submit_button:
    
    # Add pipeline status
    status = st.status(label="Starting Analysis...")
    def update_progress(message, state="running"):
        status.update(label=message, state=state)

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

    # Call orchestrator
    context = run_pipeline(text, file_metadata, progress=update_progress)

    update_progress("Analysis Complete!", "complete")

   # ---- Overall Resume Score -----
    st.divider()
    with st.container(border=True):
        st.header("Overall Resume Score")  

        col1, col2, col3 = st.columns(3)
        with col1:
            ats_score = context['ats']['ats_score']
            color = "green" if ats_score >= 5 else "red"
            st.metric(label="ATS",
                      value=f":{color}[{ats_score} / 10]",
                      border=True,
                    )

        with col2:
            exp_score = context["analysis"]['experience_level']
            color = "green" if exp_score >= 5 else "red"
            st.metric(label="Experience",
                      value=f":{color}[{exp_score} / 10]",
                      border=True,
                    )

        with col3:
            skill_score = context["skills"]["skill_score"]
            color = "green" if skill_score >= 5 else "red"
            st.metric(label="Skills",
                      value=f":{color}[{skill_score} / 10]",
                      border=True,
                    )

    # ---- Resume Analysis -----
    with st.container(border=True):
        st.header("Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.success("Strengths")
            for s in context["analysis"]["strengths"]:
                st.write(f"✓ {s}")

        with col2:
            st.warning("Weaknesses")
            for w in context["analysis"]["weaknesses"]:
                st.write(f"⚠ {w}")

        if context["analysis"].get("missing_sections"):
            st.subheader("Missing Sections:")
            for m in context["analysis"]["missing_sections"]:
                st.write(f"• {m}")

        if context["analysis"].get("formatting_issues"):
            st.subheader("Formatting Issues:")
            for i in context["analysis"]["formatting_issues"]:
                st.write(f"• {i}")

    # ---- Skill Gap -----
    with st.container(border=True):
        st.header("Skills")

        col1, col2 = st.columns(2)
        with col1:
            st.success("Current Skills")
            for s in context["skills"]["current_skills"]:
                st.write(f"• {s}")

        with col2:
            st.warning("Missing Skills") # Maybe replace with "hidden talents" ie skills you have based on projects but not added since this overlaps with suggestions maybe with st.caption("+ Add to Resume")
            for w in context["skills"]["missing_resume_skills"]:
                st.write(f"• {w}")

        st.subheader("Suggested Learning")
        st.caption("How to upskill ⬆")
        for suggestion in context["skills"]["recommended_future_skills"]:
            st.write("Skill: ", suggestion['skill'])
            st.write(f"Reason: {suggestion['reason']}")
            st.write(f"Priority: ",suggestion['priority'])

    # ---- ATS Score + Analysis (RAG Agent) ----
    with st.container(border=True):
        st.header("ATS Analysis")

        st.metric("Score:", f"{context['ats']['ats_score']} / 10")
        st.write(context["ats"]["analysis"])

        st.subheader("Issues: ")
        for i in context["ats"]["issues"]:
            st.write(f"• {i}")

        st.subheader("Improvements: ")
        for i in context["ats"]["improvements"]:
            st.write(f"• {i}")

        with st.expander("Retrieved ATS Knowledge"):
            for doc in context["ats"]["retrieved_context"]:
                st.markdown(f"**{doc['source']}**")
                st.caption(doc["section"])
                st.write(doc["content"])

    # ---- Suggest Projects (Agent + Function Calling: Google Search)

    # ---- Resume Improvement (RAG Agent) ----

    # ---- Button with Resume rewrite Agent ----

    # ---- Search Job section (More fields asking about needs + Agent + Function Calling: Google Search+Adzuna+RemoteOk)-----

    # ---- Job Description section (Match Score + Improvements + Resume Tailoring)