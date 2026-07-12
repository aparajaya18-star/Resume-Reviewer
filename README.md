# Resume Reviewer

An AI-powered resume review application built with Streamlit and Google's Gemini API.

The application uses a multi-agent architecture to analyze resumes, identify strengths and weaknesses, evaluate ATS compatibility using Retrieval-Augmented Generation (RAG), and recommend skills for career growth.

---

## Features

- Resume upload (PDF)
- Multi-agent resume analysis
- ATS compatibility evaluation using RAG
- Skill gap analysis
- Structured JSON outputs from every agent
- Modular agent-based architecture
- Streamlit web interface

---

## Architecture

```text
                     PDF Resume
                          │
                          ▼
                  PDF Text Extraction
                          │
                          ▼
                  Orchestrator Pipeline
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 Information        Resume Analysis     Skill Gap
 Extraction             Agent             Agent
        │                 │                  │
        └──────────────┬──┴──────────────────┘
                       ▼
                  Shared Context
                       │
                       ▼
             ATS RAG Retrieval Agent
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
     ChromaDB                 ATS Knowledge Base
       Vector DB                 (Markdown Docs)
                       │
                       ▼
               Final Resume Report
```

---

## Project Structure

```text
Resume Reviewer/
│
├── app.py
├── orchestrator.py
├── requirements.txt
├── README.md
│
├── agents/
│   ├── information_extraction.py
│   ├── resume_analysis.py
│   ├── skill_gap.py
│   └── ats_agent.py
│
├── rag/
│   ├── database.py
│   └── build_db.py
│
├── utils/
│   ├── gemini.py
│   ├── pdf.py
│   ├── builder.py
│   └── ...
│
├── knowledge_base/
│   └── ats/
│
└── data/
```

---

## Agent Pipeline

### 1. Information Extraction Agent

Extracts structured candidate information including:

- Career stage
- Technical domain
- Experience
- Education
- Skills
- Projects
- Achievements

---

### 2. Resume Analysis Agent

Provides an overall review by identifying:

- Strengths
- Weaknesses
- Missing sections
- Formatting issues
- Experience level

---

### 3. Skill Gap Agent

Evaluates the candidate's technical profile and returns:

- Skill score
- Current skills
- Missing resume skills
- Recommended future skills

---

### 4. ATS Review Agent (RAG)

Uses Retrieval-Augmented Generation.

Workflow:

1. Build a search query from previous agent outputs.
2. Retrieve relevant ATS guidance from ChromaDB.
3. Combine retrieved context with resume analysis.
4. Generate ATS score and improvement suggestions.

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- ChromaDB
- PyMuPDF
- Markdown Knowledge Base

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd Resume-Reviewer
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```text
GEMINI_API_KEY=your_api_key_here
```

---

## Build the Vector Database

Before running the application, build the ATS knowledge base.

```bash
python build_db.py
```

---

## Run

```bash
streamlit run app.py
```

---

## Future Improvements

- Project recommendation agent
- Resume rewrite agent
- Job search integration
- Resume tailoring for job descriptions
- Parallel execution of independent agents
- Enhanced UI/UX
- Deployment optimizations

---

## License

This project was developed as part of a Generative AI and Agentic AI bootcamp and is intended for educational purposes.