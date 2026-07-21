import streamlit as st
from google.genai.errors import ClientError

from utils.pdf import load_pdf
from utils.timer import timed_step
from orchestrator import run_pipeline
from agents.project_recommendation import project_recommendation_agent
from agents.resume_rewrite import rewrite_agent

def format_resume(resume):
    output = []

    header = resume["header"]

    output.append(header["name"])

    if header.get("headline"):
        output.append(header["headline"])

    contact = " | ".join(filter(None, [
        header.get("location"),
        header.get("phone"),
        header.get("email")
    ]))

    output.append(contact)

    if header.get("links"):
        output.append(
            " | ".join(
                f"{l['label']}: {l['url']}"
                for l in header["links"]
            )
        )

    output.append("")
    output.append(resume["professional_summary"])
    output.append("")

    for section in resume["sections"]:

        output.append(section["title"])
        output.append("-" * len(section["title"]))

        match section["section_type"]:

            case "paragraphs":
                output.extend(section["content"])

            case "bullets":
                for bullet in section["content"]:
                    output.append(f"• {bullet}")

            case "education":
                for edu in section["content"]:
                    output.append(edu["institution"])
                    output.append(edu["degree"])

                    if edu.get("duration"):
                        output.append(edu["duration"])

                    for detail in edu.get("details", []):
                        output.append(f"• {detail}")

                    output.append("")

            case "experience":
                for exp in section["content"]:
                    output.append(
                        f"{exp['role']} | {exp['company']}"
                    )

                    if exp.get("duration"):
                        output.append(exp["duration"])

                    for bullet in exp["bullets"]:
                        output.append(f"• {bullet}")

                    output.append("")

            case "projects":
                for project in section["content"]:
                    output.append(project["name"])

                    if project.get("tech_stack"):
                        output.append("Tech: " + ", ".join(project["tech_stack"]))

                    for bullet in project["bullets"]:
                        output.append(f"• {bullet}")

                    output.append("")

            case "skills":
                for group in section["content"]:
                    output.append(
                        f"{group['category']}: "
                        + ", ".join(group["items"])
                    )

        output.append("")

    return "\n".join(output)

# ----- Sreamlit app -----

# Configure Streamlit app
st.set_page_config(
    page_title="Resume Reviewer",
    layout="wide"
)
st.markdown(
    "<div style='height:20px'></div>",
    unsafe_allow_html=True
)

left, center, right = st.columns([1,16,1])

with center:
    st.markdown("<h1 style='text-align: center;'>Resume Reviewer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div style='height:3px'></div>",
        unsafe_allow_html=True
    )
    with st.container(border=True):

        st.subheader("📄 Upload Resume")
        st.caption(
            "Upload a PDF resume to receive AI-powered feedback."
        )

        st.write("")

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
    text, num_pages = timed_step("Load PDF", load_pdf, uploaded_file)
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
    st.session_state.pop("context", None)
    st.session_state.context = timed_step("Complete Pipeline", run_pipeline,text, file_metadata, progress=update_progress)

    update_progress("Analysis Complete!", "complete")

   
if "context" in st.session_state:
    with st.container(border=True, key="toolbox"):
        st.markdown("""
        <h3 style="
        text-align:center;
        color:#8fb4ff;
        margin-bottom:0.5rem;">
        Additional Tools
        </h3>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            project_button = st.button("Recommend Portfolio Projects", use_container_width=True)
        with col2:
            rewrite_button = st.button("Rewrite Resume", use_container_width=True)

    context = st.session_state.context
    with st.expander(expanded=True, label="📊 Resume Analysis"):
        # ---- Overall Resume Score -----
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
        with st.expander("Overview",expanded=True):
            st.subheader("Summary")
            st.write(context["analysis"]["summary"])

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
        with st.expander("Skills",expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.success("Current Skills")
                for s in context["parsed"]["identified_skills"]:
                    st.write(f"• {s}")

            with col2:
                st.warning("Resume Skill Gaps") 
                st.caption("Add to Resume +")
                for w in context["skills"]["resume_skill_gaps"]:
                    st.write(f"• {w}")

            st.subheader("Suggested Learning")
            st.caption("How to upskill ⬆")

            recommendations = context["skills"]["recommended_skills"]
            for i in range(0, len(recommendations), 2):
                col1, col2 = st.columns(2)

                with col1.container(border=True, height=220):
                    suggestion = recommendations[i]
                    st.markdown(f"### {suggestion['skill']}")
                    st.caption(
                        f"{suggestion['category']} • {suggestion['priority']} Priority"
                    )
                    st.write(suggestion["reason"])

                if i + 1 < len(recommendations):
                    with col2.container(border=True, height=220):
                        suggestion = recommendations[i + 1]
                        st.markdown(f"### {suggestion['skill']}")
                        st.caption(
                            f"{suggestion['category']} • {suggestion['priority']} Priority"
                        )
                        st.write(suggestion["reason"])

        # ---- ATS Score + Analysis (RAG Agent) ----
        with st.expander("ATS Analysis",expanded=True):
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
    if project_button:
        if not context.get("projects"):
            with st.spinner("Searching for suitable projects..."):
                try:
                    context["projects"] = timed_step("Complete Project rec",project_recommendation_agent,context)
                except ClientError as e:
                    context["projects"] = {
                        "error": str(e)
                    }

            st.session_state.context = context

    if st.session_state.context.get("projects"):
        projects = st.session_state.context["projects"]
        with st.expander(expanded=True, label="💡 Project Recommendations"):
            st.header("Project Recommendations")
            if isinstance(projects, dict) and "error" in projects:
                st.warning(projects["error"])
            else:
                for p in projects:
                    with st.container(border=True):
                        st.subheader(p["title"])
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(label="Difficulty", value=p["difficulty"], border=True)
                        with col2:
                            st.metric(label="Time", value=p["time_estimate"], border=True)
                        with col3:
                            st.metric(label="Portfolio Impact", value=f"{p['portfolio_impact']} / 10", border=True)

                        st.write(p["overview"])

                        st.caption("Why this project?")
                        st.write(p["why_now"])

                        st.caption("Skills")
                        for skill in p["skills"]:
                            st.write(f"• {skill}")

                        with st.expander("Resources", expanded=True):
                            for resource in p["resources"]:
                                st.markdown(f"- [{resource['title']}]({resource['url']})")

    # ---- Resume rewrite Agent ----
    if rewrite_button:
        if not context.get("rewrite"):
            with st.spinner("Rewriting Resume..."):
                try:
                    context["rewrite"] = rewrite_agent(context)
                except ClientError as e:
                    context["rewrite"] = {
                        "error": str(e)
                    }

            st.session_state.context = context

    if st.session_state.context.get("rewrite"):
        resume_info = st.session_state.context["rewrite"]
        resume = resume_info["rewritten_resume"]

        with st.expander(expanded=True, label="📝 Resume Rewrite"):
            st.header("Rewritten Resume")

            overview = resume_info["overview"]

            with st.container(border=True):
                st.info(
                    f"**{overview['resume_quality']}**\n\n"
                    f"{overview['summary']}"
                )

                if overview["major_changes"]:
                    st.subheader("Major Improvements")
                    for change in overview["major_changes"]:
                        st.markdown(f"- {change}")

            formatted = format_resume(resume)
            st.download_button(
                "📥 Download Rewritten Resume",
                formatted,
                "rewritten_resume.txt",
                mime="text/plain",
                use_container_width=True
            )

            header = resume["header"]

            st.markdown(f"# {header['name']}")

            if header.get("headline"):
                st.caption(header["headline"])

            st.write(
                " | ".join(
                    filter(
                        None,
                        [
                            header["location"],
                            header["phone"],
                            header["email"]
                        ]
                    )
                )
            )

            if header["links"]:
                cols = st.columns(len(header["links"]))

                for col, link in zip(cols, header["links"]):
                    col.link_button(link["label"], link["url"])

            st.write(resume["professional_summary"])

            for section in resume["sections"]:
                st.markdown(f"## {section['title']}")

                match section["section_type"]:

                    case "paragraphs":
                        for paragraph in section["content"]:
                            st.write(paragraph)

                    case "bullets":
                        for bullet in section["content"]:
                            st.markdown(f"- {bullet}")

                    case "education":
                        for edu in section["content"]:
                            st.markdown(f"**{edu['institution']}**")
                            st.write(edu["degree"])

                            if edu.get("duration"):
                                st.caption(edu["duration"])

                            for detail in edu.get("details", []):
                                st.markdown(f"- {detail}")

                    case "experience":
                        for exp in section["content"]:
                            col1, col2 = st.columns([4,1])

                            with col1:
                                st.markdown(f"**{exp['role']}**")
                                st.write(exp["company"])

                            with col2:
                                if exp.get("duration"):
                                    st.caption(exp["duration"])

                            for bullet in exp["bullets"]:
                                st.markdown(f"- {bullet}")

                    case "projects":
                        for project in section["content"]:
                            st.markdown(f"**{project['name']}**")

                            if project.get("tech_stack"):
                                st.caption(" • ".join(project["tech_stack"]))

                            for bullet in project["bullets"]:
                                st.markdown(f"- {bullet}")

                    case "skills":
                        for group in section["content"]:
                            skills = " • ".join(group["items"])
                            st.markdown(f"**{group['category']}:** {skills}")
        
            col1, col2 = st.columns(2)
            with col1:
                with st.expander(label="Additional Tips",expanded=True):
                    for tip in resume_info["additional_tips"]:
                        st.markdown(
                            f"**{tip['priority']} Priority** — {tip['tip']}"
                        )

            with col2:
                with st.expander(label="Changes",expanded=True):
                    for change in resume_info["changes"]:
                        with st.container(border=True):

                            st.markdown(
                                f"### {change['section']} ({change['severity']})"
                            )
                            st.error(change["original"], icon="❌")
                            st.success(change["improved"], icon="✅")
                            st.caption(change["reason"])

    # ---- Search Job section (More fields asking about needs + Agent + Function Calling: Google Search+Adzuna+RemoteOk)-----

    # ---- Job Description section (Match Score + Improvements + Resume Tailoring)