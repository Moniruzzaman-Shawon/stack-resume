# Stack Resume

AI-powered resume reviewer built with React, Django, and Google Gemini.

Upload a PDF resume and get structured feedback: strengths, weaknesses, missing skills, actionable suggestions, and an overall score.

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS v4
- **Backend:** Django + Django REST Framework
- **AI:** LangChain + Google Gemini (`gemini-2.0-flash`)
- **PDF parsing:** pypdf

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env from example and add your API key
cp ../.env.example .env
# Edit .env and set GOOGLE_API_KEY

python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and proxies API requests to the Django backend on port 8000.

## Environment Variables

Set these in `backend/.env`:

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key |
| `DEBUG` | `True` for development |
| `DJANGO_SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |

## Running Tests

```bash
cd backend
$env:DJANGO_SETTINGS_MODULE="config.test_settings"
python manage.py test
```

## Project Structure

```
Stack-Resume/
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── test_settings.py
│   │   └── urls.py
│   ├── resume_review/
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   └── pdf_service.py
│   │   └── tests/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   ├── context/
│   │   └── types.ts
│   ├── vite.config.ts
│   └── package.json
├── .env.example
└── plan.md
```
