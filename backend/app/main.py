from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import questions, users, learn, exam, exam_evaluation_single_answers

app = FastAPI(title="EchoLearn API", docs_url="/docs")

# ---------------------------
# CORS konfigurieren
# ---------------------------
origins = ["http://localhost:5173"]  # Vite Dev Server

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

# ---------------------------
# Router einbinden
# ---------------------------
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(learn.router)
app.include_router(exam.router)
app.include_router(exam_evaluation_single_answers.router)
