# Common ATS Parsing Problems

This guide describes common resume formatting issues that can prevent Applicant Tracking Systems (ATS) from correctly reading or parsing a resume. Each issue includes an explanation and a recommended solution.

---

# Two-Column Layouts

## Problem

Content from multiple columns may become mixed together after parsing.

Example:

- Skills appear beside unrelated work experience.
- Job titles become separated from achievements.
- Sections appear in the wrong order.

## Why It Happens

Many ATS platforms convert resumes into plain text by reading from left to right and top to bottom. Two-column layouts often lose their visual structure during this conversion.

## Recommendation

- Use a single-column resume layout.
- Stack sections vertically.
- Keep information in a natural reading order.

---

# Tables Used for Layout

## Problem

Information inside tables may become separated or reordered.

Example:

- Dates become detached from job titles.
- Company names appear in incorrect positions.
- Bullet points lose their associated role.

## Why It Happens

Many ATS platforms remove table formatting before extracting text, causing individual table cells to be read independently.

## Recommendation

Avoid using tables to organize resume content.

Instead, write entries as plain text.

Example:

Software Engineer | ABC Technologies  
Jan 2023 – Present

---

# Headers and Footers

## Problem

Important information such as your name or contact details may not be extracted.

## Why It Happens

Many ATS systems ignore document headers and footers during parsing.

## Recommendation

Place all contact information inside the main body of the document.

Include:

- Name
- Phone number
- Email
- LinkedIn
- Portfolio or GitHub

---

# Custom Section Titles

## Problem

The ATS may fail to recognize important resume sections.

Examples of poor section titles:

- My Journey
- Career Story
- What I Do
- Things I Built

## Why It Happens

Most ATS platforms identify resume sections using standard keywords.

## Recommendation

Use conventional headings such as:

- Professional Summary
- Work Experience
- Education
- Skills
- Projects
- Certifications
- Awards

---

# Decorative Fonts

## Problem

Some characters may appear incorrectly after parsing.

Symptoms include:

- Missing letters
- Boxes replacing characters
- Corrupted words

## Why It Happens

Certain decorative fonts are unavailable on ATS servers, forcing font substitution.

## Recommendation

Use standard fonts:

- Arial
- Calibri
- Helvetica
- Cambria
- Times New Roman
- Garamond

---

# Text Inside Images

## Problem

Text displayed as images cannot be extracted by most ATS platforms.

Examples include:

- Skill bars
- Icons containing text
- Infographic resumes
- Graphic timelines

## Why It Happens

Most ATS systems extract text rather than performing Optical Character Recognition (OCR).

## Recommendation

Represent all important information as selectable text.

Never place:

- Skills
- Experience
- Contact information
- Certifications

inside images.

---

# Image-Based PDFs

## Problem

The ATS cannot extract any resume content.

## Why It Happens

Scanned PDFs contain images instead of machine-readable text.

## Recommendation

Export resumes directly from Word or Google Docs as text-based PDFs.

A quick check:

If you cannot highlight individual words in the PDF, it is probably image-based.

---

# Inconsistent Date Formats

## Problem

Employment history may be parsed incorrectly.

Examples:

- Jan 2024
- 01/2024
- '24
- Present
- Current

Mixing formats can confuse parsers.

## Recommendation

Choose one format and use it consistently.

Recommended:

- Jan 2024 – Present
- January 2024 – Present

---

# Special Characters

## Problem

Symbols may be removed or replaced during parsing.

Examples include:

- ★
- ✔
- ➜
- ◆
- ➤

## Recommendation

Use standard characters instead.

Preferred:

- Standard bullet points
- Simple hyphens
- Plain quotation marks

---

# Acronyms Without Expansion

## Problem

Keyword matching may fail.

Example:

Resume contains:

FP&A

Job description contains:

Financial Planning and Analysis

The ATS may not recognize these as equivalent.

## Recommendation

Write the complete term once before using the abbreviation.

Example:

Financial Planning and Analysis (FP&A)

Representational State Transfer (REST)

Search Engine Optimization (SEO)

---

# Hyperlinks Without Descriptive Text

## Problem

Some ATS platforms extract raw URLs but ignore embedded hyperlink labels.

## Recommendation

Display important links clearly.

Example:

GitHub:
https://github.com/username

Portfolio:
https://portfolio.com

Avoid hiding important links behind generic text such as:

- Click here
- My website

---

# Excessive Graphics and Icons

## Problem

Logos, icons, rating bars, timelines, and decorative graphics may interfere with parsing.

## Recommendation

Use graphics sparingly.

Keep all critical resume information in plain text.

---

# ATS Parsing Checklist

Before submitting a resume, verify that it:

- Uses a single-column layout.
- Does not rely on tables.
- Keeps contact information outside headers and footers.
- Uses standard section headings.
- Uses professional fonts.
- Contains selectable text.
- Uses consistent date formatting.
- Avoids unnecessary graphics.
- Expands important acronyms.
- Exports as a text-based PDF.