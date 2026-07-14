# Architecture

## Overview

The Resume Analyzer is designed as an **agentic AI system** rather than a single large prompt.

Instead of asking one LLM to perform every task simultaneously, the application divides the workflow into specialized agents that communicate through a shared context object.

This approach improves:
- modularity
- maintainability
- consistency
- scalability
- prompt quality

---

# High-Level Workflow

```
Resume PDF
     │
     ▼
Load & Extract Text
     │
     ▼
Information Extraction Agent
     │
     ▼
Resume Analysis Agent
     │
 ┌───┴────────────┐
 ▼                ▼
Skill Agent    ATS Agent (RAG)
 └────┬──────────┘
      ▼
Project Recommendation Agent
      ▼
Final Results
```

---

# Shared Context

Each agent contributes to a cumulative context object.

```python
context = {
    "input": {},
    "parsed": {},
    "analysis": {},
    "skills": {},
    "ats": {},
    "projects": {}
}
```

Rather than passing the entire context to every agent, a context builder provides each agent with only the information relevant to its task.

This keeps prompts concise and minimizes unnecessary token usage.

---

# Agent 1 — Information Extraction

## Purpose

Extract structured information from the resume.

Outputs include:

- candidate profile
- education
- work experience
- projects
- skills
- certifications
- achievements
- professional links

This agent acts as the foundation for the rest of the workflow.

---

# Agent 2 — Resume Analysis

Consumes the structured resume information and performs recruiter-style evaluation.

Outputs include:

- strengths
- weaknesses
- experience score
- executive summary
- formatting issues
- missing sections

This separates factual extraction from subjective evaluation.

---

# Agent 3 — Skill Gap Analysis

Evaluates the candidate's technical profile.

Produces:

- skill score
- resume skill gaps
- recommended technologies
- learning priorities

The recommendations are personalized using:

- career stage
- education
- projects
- work experience
- existing skills
- previous analysis

---

# Agent 4 — ATS Analysis (RAG)

Unlike the previous agents, ATS recommendations are grounded using Retrieval-Augmented Generation.

## Pipeline

```
Resume
   │
Generate Query
   │
Retrieve Documents
   │
Relevant ATS Context
   │
Gemini
   │
ATS Analysis
```

The agent combines:

- parsed resume information
- previous analysis
- retrieved ATS guidance

to produce grounded ATS recommendations instead of relying solely on model memory.

---

# Retrieval-Augmented Generation

The ATS knowledge base is indexed inside ChromaDB.

Pipeline:

```
ATS Documents
      │
Chunking
      │
Embedding
      │
Vector Database
      │
Semantic Search
      │
Relevant Chunks
      │
ATS Agent
```

Benefits:

- grounded responses
- easier knowledge updates
- reduced hallucinations

---

# Project Recommendation Workflow

Project recommendation uses a three-stage agent pipeline.

## Stage 1 — Planning

The LLM generates several focused search queries based on:

- candidate profile
- experience
- projects
- skills
- skill gaps

---

## Stage 2 — Web Search

Generated queries are sent to the Tavily Search API.

Results are:

- collected
- deduplicated
- ranked
- filtered

Preference is given to high-quality technical resources such as:

- GitHub
- Hugging Face
- Kaggle
- Official Documentation

---

## Stage 3 — Project Selection

The final agent receives:

- candidate information
- learning goals
- filtered search results

It selects projects that maximize:

- portfolio value
- resume impact
- skill development
- originality

---

# Parallel Execution

After Resume Analysis completes, two independent agents execute concurrently.

```
Resume Analysis
      │
 ┌────┴────┐
 ▼         ▼
Skill     ATS
```

Using `ThreadPoolExecutor` reduces overall pipeline latency since these agents have no dependency on each other.

---

# Structured Outputs

Every LLM response is constrained using JSON schemas.

Benefits:

- predictable outputs
- simpler parsing
- reliable communication between agents
- easier debugging

---

# Design Decisions

## Specialized Agents

Each agent performs one well-defined responsibility.

This keeps prompts smaller and improves consistency.

---

## Context Builder

Only task-specific information is passed to each agent.

Advantages:

- lower token usage
- clearer prompts
- better separation of concerns

---

## Task-specific temperature tuning

Different agents use different sampling temperatures depending on their role. 

Deterministic parsing and RAG-based evaluation use lower temperatures for consistency and factual grounding, while creative tasks such as search query generation use higher temperatures to encourage diverse and relevant recommendations.

---

## Modular Components

Each agent can be developed, tested, and replaced independently without affecting the rest of the pipeline.

---

# Future Work

Potential extensions include:

- Resume rewriting agent
- Job description matching
- Resume tailoring
- Cover letter generation
- Interview preparation
- Multiple RAG knowledge bases
- Local embedding models
- Support for additional resume formats

---

## Deployment

The application is deployed using Streamlit Community Cloud.

Live Demo:
https://resume-reviewer-18.streamlit.app/

---

# Summary

The project demonstrates the integration of several modern AI engineering concepts:

- Large Language Models
- Prompt Engineering
- Agentic Workflows
- Retrieval-Augmented Generation (RAG)
- Structured Outputs
- Semantic Search
- Parallel Agent Execution
- Web Search Integration

These components work together to produce grounded, modular, and personalized resume analysis.