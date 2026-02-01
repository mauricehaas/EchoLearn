from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import exam, exam_evaluation_single_answers, questions, users

app = FastAPI(title="EchoLearn API", docs_url="/docs")

# ---------------------------
# CORS konfigurieren
# ---------------------------
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]  # Vite Dev Server

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Erlaubte Domains
    allow_credentials=True,  # nötig für Cookies/Headers
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Content-Type, Authorization etc.
)

# ---------------------------
# Router einbinden
# ---------------------------
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(exam.router)
app.include_router(exam_evaluation_single_answers.router)
