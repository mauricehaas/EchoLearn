import asyncio

import pandas as pd

from app.core.db import Base, async_session, engine
from app.models.exam_evaluation_final import ExamEvaluationFinal  # noqa: F401
from app.models.exam_evaluation_single_answer import (
    ExamEvaluationSingleAnswer,  # noqa: F401
)
from app.models.question import Question

PROCESSED_QUESTIONS_PATH = "data/processed/questions.csv"
BATCH_SIZE = 50


async def seed():
    print("Creating tables…")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Loading processed questions…")
    df = pd.read_csv(PROCESSED_QUESTIONS_PATH)

    async with async_session() as session:
        exam_evaluation_final = []

        exam_evaluation_single_answer = []

        session.add_all(exam_evaluation_final + exam_evaluation_single_answer)
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
