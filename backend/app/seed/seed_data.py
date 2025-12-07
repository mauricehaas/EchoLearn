import asyncio

from app.core.db import Base, async_session, engine
from app.models.exam_evaluation_final import ExamEvaluationFinal
from app.models.exam_evaluation_single_answer import ExamEvaluationSingleAnswer
from app.models.question import Question
from app.models.user import User


async def seed():
    print("Creating tables…")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # optional, nur für Dev
        await conn.run_sync(Base.metadata.create_all)

    print("Seeding data…")
    async with async_session() as session:
        # Fragen + Antworten
        questions = [
            Question(question="Was ist 2 + 2?", answer="4"),
            Question(question="Was ist die Hauptstadt von Frankreich?", answer="Paris"),
            Question(question="Wie viele Kontinente gibt es?", answer="7"),
            Question(question="Was ist 10 geteilt durch 2?", answer="5"),
            Question(
                question="Welche Farbe hat der Himmel an einem sonnigen Tag?",
                answer="Blau",
            ),
            Question(question="Wie viele Tage hat ein Schaltjahr?", answer="366"),
            Question(question="Wer schrieb 'Faust'?", answer="Goethe"),
            Question(question="Wie viele Planeten hat unser Sonnensystem?", answer="8"),
            Question(question="Was ist das Symbol für Wasserstoff?", answer="H"),
            Question(
                question="Welches Tier ist das größte auf der Erde?", answer="Blauwal"
            ),
            Question(question="Wie viele Minuten hat eine Stunde?", answer="60"),
            Question(question="Was ist 7 mal 6?", answer="42"),
            Question(question="Wie viele Bundesländer hat Deutschland?", answer="16"),
            Question(question="Wer malte die Mona Lisa?", answer="Leonardo da Vinci"),
            Question(question="Wie viele Seiten hat ein Würfel?", answer="6"),
            Question(question="Was ist die Hauptstadt von Italien?", answer="Rom"),
            Question(
                question="Wie viele Zähne hat ein Erwachsener normalerweise?",
                answer="32",
            ),
            Question(question="Was ist 15 minus 7?", answer="8"),
            Question(
                question="Welche Sprache wird in Brasilien gesprochen?",
                answer="Portugiesisch",
            ),
            Question(
                question="Was ist die chemische Formel von Kochsalz?", answer="NaCl"
            ),
        ]

        # Beispiel-User
        users = [
            User(username="admin", password_hash="hashed123", role="admin"),
            User(username="user", password_hash="hashed456", role="user"),
        ]

        session.add_all(questions + users)
        await session.commit()

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
