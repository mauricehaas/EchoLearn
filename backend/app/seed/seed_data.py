import asyncio

from app.core.db import Base, async_session, engine
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
            Question(
                question="Was ist 1+1?",
                answer="2",
            ),
            Question(
                question="Was sind die wichtigsten Schritte im Data-Science-Prozess?",
                answer="Die wichtigsten Schritte umfassen typischerweise Problemdefinition, Datensammlung, Datenaufbereitung, explorative Datenanalyse, Modellierung, Evaluation und Deployment.",
            ),
            Question(
                question="Was ist 2+2 und was ist 4+4?",
                answer="2+2 ist 4 und 4+4 ist 8",
            ),
        ]

        # Beispiel-User
        users = [
            User(username="admin", password_hash="hashed123", role="admin"),
            User(username="user", password_hash="hashed456", role="user"),
        ]

        exam_evaluation_final = []

        exam_evaluation_single_answer = []

        session.add_all(
            questions + users + exam_evaluation_final + exam_evaluation_single_answer
        )
        await session.commit()

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
