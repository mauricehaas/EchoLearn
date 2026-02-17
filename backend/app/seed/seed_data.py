import asyncio

import pandas as pd

from app.core.db import Base, async_session, engine
from app.models.exam_evaluation_final import ExamEvaluationFinal  # noqa: F401
from app.models.question import Question
from app.models.user import User

PROCESSED_QUESTIONS_PATH = "data/processed/questions.csv"
BATCH_SIZE = 50


async def seed() -> None:
    """Seed the database with initial data."""
    print("Creating tables…")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Loading processed questions…")
    df = pd.read_csv(PROCESSED_QUESTIONS_PATH)

    async with async_session() as session:
        users = [
            User(username="admin", password_hash="hashed123", role="admin"),
            User(username="user", password_hash="hashed456", role="user"),
        ]

        exam_evaluation_final = []

        exam_evaluation_single_answer = []

        session.add_all(users + exam_evaluation_final + exam_evaluation_single_answer)
        await session.commit()

        questions = [
            Question(
                question=row["question"],
                answer=row["answer"],
                max_points=str(row["max_points"]),
            )
            for _, row in df.iterrows()
        ]

        for i in range(0, len(questions), BATCH_SIZE):
            batch = questions[i : i + BATCH_SIZE]
            session.add_all(batch)
            await session.commit()
            print(f"Inserted questions {i + 1}-{i + len(batch)}")

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
