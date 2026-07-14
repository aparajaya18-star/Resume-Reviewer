# AI Resume Analyzer

An AI-powered resume analysis application that uses **agentic workflows**, **Retrieval-Augmented Generation (RAG)**, **LLMs**, and **web search** to provide personalized resume feedback and portfolio recommendations.

The application analyzes a resume PDF, evaluates its strengths and weaknesses, identifies skill gaps, reviews ATS compatibility using a dedicated knowledge base, and recommends portfolio projects tailored to the candidate's background.

## Live Demo

🌐 **Streamlit App:** https://resume-reviewer-18.streamlit.app/

---

## Features

### Resume Parsing
- Extracts structured information from uploaded resumes
- Identifies:
  - Candidate profile
  - Education
  - Work experience
  - Skills
  - Projects
  - Certifications
  - Achievements
  - Professional links

### Resume Analysis
Provides recruiter-style feedback including:
- Executive summary
- Resume strengths
- Resume weaknesses
- Experience score
- Missing resume sections
- Formatting suggestions

### Skill Gap Analysis
Evaluates the candidate's technical profile and provides:
- Skill score
- Resume skill gaps
- Personalized learning recommendations
- Prioritized technologies to learn

### ATS Analysis (RAG)
Uses Retrieval-Augmented Generation with a curated ATS knowledge base to evaluate:
- ATS compatibility score
- Formatting issues
- Missing sections
- Keyword coverage
- Actionable ATS improvements

### Portfolio Project Recommendation
Uses a multi-step agent workflow to:
- Generate intelligent search queries
- Search the web for high-quality project ideas
- Filter duplicate and low-quality resources
- Recommend portfolio projects tailored to the candidate

---

## Architecture Overview

```
                Resume PDF
                     │
                     ▼
             Information Extraction
                     │
                     ▼
              Resume Analysis
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Skill Gap Agent          ATS RAG Agent
        └────────────┬────────────┘
                     ▼
             Project Planner
                     ▼
             Web Search (Tavily)
                     ▼
           Project Selection Agent
                     ▼
            Final Recommendations
```

A more detailed explanation is available in **ARCHITECTURE.md**.

---

## Technologies Used

### AI
- Google Gemini
- Structured JSON Output
- Prompt Engineering

### RAG
- ChromaDB
- Gemini Embeddings
- Semantic Retrieval

### Backend
- Python
- Streamlit

### Search
- Tavily Search API

### Concurrency
- ThreadPoolExecutor

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd resume-analyzer
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GEMINI_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Run the application

```bash
streamlit run app.py
```

---

## Project Structure

```
resume-analyzer/
│
├── agents/
│   ├── information_extraction.py
│   ├── resume_analysis.py
│   ├── skill_gap.py
│   ├── ats_agent.py
│   └── project_recommendation.py
│
├── rag/
│   ├── database.py
│   └── ...
│
├── utils/
│
├── orchestrator.py
├── app.py
├── README.md
└── ARCHITECTURE.md
```

---

## Future Improvements

- Resume rewriting agent
- Job matching
- Resume tailoring for job descriptions
- Interview preparation agent
- Cover letter generation
- Additional knowledge bases
- Support for DOCX resumes

---

## License

This project was developed as the final capstone project for the TDA Gen AI and Agentic AI Bootcamp.