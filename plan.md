# Stack Resume — AI Resume Reviewer

## Overview
Stack Resume is an AI-powered resume reviewer that analyzes uploaded PDF resumes and provides structured feedback including strengths, weaknesses, missing skills, improvement suggestions, and an overall score.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS v4 |
| Backend | Django + Django REST Framework |
| AI | LangChain + Google Gemini |
| PDF | pypdf |
| Icons | Lucide React |

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Animated Logo | Stacked layers icon + "Stack Resume" text with CSS animations |
| 2 | PDF Upload | Drag-and-drop zone, file picker, blue-600 dashed border |
| 3 | File Validation | Reject non-PDFs, reject >5MB files |
| 4 | PDF Text Extraction | pypdf in-memory processing, no disk writes |
| 5 | AI Resume Analysis | LangChain + Gemini, structured JSON response |
| 6 | Score Gauge | Circular progress ring, color-coded (green/yellow/red) |
| 7 | Section Cards | Strengths, Weaknesses, Missing Skills, Suggestions |
| 8 | Modern Spinner | Orbital arcs animation + pulsing center + text |
| 9 | Dark/Light Theme | Toggle with localStorage persistence |
| 10 | Loading States | Spinner during analysis, skeleton states |
| 11 | Error Handling | Toast/banner for errors, file validation messages |
| 12 | Responsive Design | Mobile-first, stacks on small screens |
| 13 | Rate Limiting | 5 requests/hour per IP |
| 14 | Security Headers | CSP, CSRF, MIME validation |
| 15 | Environment Config | .env for API keys, .gitignore protection |

## Project Structure

```
Stack-Resume/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── resume_review/
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── services/
│   │       ├── pdf_service.py
│   │       └── ai_service.py
│   └── static/frontend/
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   ├── context/
│   │   │   └── ThemeContext.tsx
│   │   ├── components/
│   │   │   ├── AnimatedLogo.tsx
│   │   │   ├── ThemeToggle.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── ReviewResults.tsx
│   │   │   ├── ScoreGauge.tsx
│   │   │   ├── SectionCard.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   └── types.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
│
├── .gitignore
├── .env.example
└── plan.md
```

## UI Design System

### Color Palette (Tailwind)

| Role | Light Mode | Dark Mode |
|------|-----------|-----------|
| Background | bg-white | bg-gray-950 |
| Surface/Cards | bg-gray-50 | bg-gray-900 |
| Elevated Surface | bg-white | bg-gray-800 |
| Primary | blue-600 | blue-500 |
| Primary hover | blue-700 | blue-400 |
| Text primary | text-gray-900 | text-gray-50 |
| Text secondary | text-gray-500 | text-gray-400 |
| Border | border-gray-200 | border-gray-800 |

### Modern UI Traits
- Rounded corners: rounded-2xl on cards, rounded-xl on buttons
- Subtle shadows: shadow-sm light mode
- Glassmorphism: backdrop-blur-sm bg-white/80 (light) / bg-gray-900/80 (dark)
- Smooth transitions: transition-all duration-300
- Gradient accents: bg-gradient-to-r from-blue-600 to-blue-500

## API Flow

```
POST /api/review/
  → Receive PDF file upload (multipart/form-data)
  → Validate file type + size
  → Extract text via pypdf (in-memory)
  → Send text to LangChain → Google Gemini
  → Structured prompt returns JSON:
      - strengths (string[])
      - weaknesses (string[])
      - missing_skills (string[])
      - suggestions (string[])
      - overall_score (int, 0-100)
  → Return JSON response
```

## Security

- GOOGLE_API_KEY in .env only, never exposed to frontend
- File upload: validate MIME type + size limit (5MB)
- In-memory PDF processing only (no disk writes)
- django-csp for Content Security Policy headers
- CSRF enabled on API view
- Rate limiting via django-ratelimit
- Text length cap before sending to Gemini

## Environment Variables

```env
GOOGLE_API_KEY=your-key-here
DEBUG=True
```

## Build Order

1. Create plan.md (this file)
2. Initialize Django project + app
3. Initialize React + Vite + Tailwind
4. Build AnimatedLogo component
5. Build Theme Context + Toggle
6. Build Modern Spinner component
7. Build FileUpload component
8. Build backend services (PDF extraction → AI analysis)
9. Build Django API endpoint
10. Build Results UI (ScoreGauge + SectionCards)
11. Build App.tsx main layout
12. Wire frontend ↔ backend
13. Security hardening
14. Configure Django to serve React build
15. End-to-end testing
