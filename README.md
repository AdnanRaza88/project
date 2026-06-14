# Student Grade Tracker

A full-stack application to track student grades with AI-powered study tips, motivation quotes, and improvement plans.

## Features
- FastAPI backend with SQLModel database
- Streamlit frontend with neumorphic design
- Groq AI integration for personalized study assistance
- CRUD operations for grades
- Railway deployment ready

## Project Structure
```
.
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── ai_service.py
│   └── requirements.txt
├── frontend/
│   ├── ui.py
│   └── requirements.txt
└── railway.toml
```

## Local Setup
1. Clone the repo
2. Create `.env` file in backend with `GROQ_API_KEY=your_key`
3. Run backend: `cd backend && uvicorn main:app --reload`
4. Run frontend: `cd frontend && streamlit run ui.py`

## Deployment
Deploy on Railway using the provided `railway.toml`.