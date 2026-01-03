import asyncio

import pandas as pd

from app.core.db import Base, async_session, engine
from app.models.question import Question
from app.models.user import User

PROCESSED_QUESTIONS_PATH = "data/processed/questions.csv"


async def seed():
    print("Creating tables…")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Loading processed questions…")
    df = pd.read_csv(PROCESSED_QUESTIONS_PATH)

    async with async_session() as session:
        questions = [
            Question(
                question=row["question"],
                answer=row["answer"],
            )
            for _, row in df.iterrows()
        ]

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
