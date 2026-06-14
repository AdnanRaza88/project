# Student Grade Tracker with AI

A full-stack Student Grade Management System with FastAPI backend and Streamlit frontend, powered by Groq AI for study tips, motivation, and improvement plans.

## Project Structure
```
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
└── README.md
```

## Local Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (new terminal)
```bash
cd frontend
export API_URL="http://localhost:8000"
pip install -r requirements.txt
streamlit run ui.py
```

## Deployment

### Backend on Railway
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Env: `GROQ_API_KEY`

### Frontend on Streamlit Cloud
- Main file path: `frontend/ui.py`
- Env: `API_URL` = Backend URL
