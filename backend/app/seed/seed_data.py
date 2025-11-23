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
            Question(question="Was ist 2 + 2?", answer="4"),
            Question(question="Was ist die Hauptstadt von Frankreich?", answer="Paris"),
        ]

        # Beispiel-User
        users = [
            User(username="admin", password_hash="hashed123", role="admin"),
            User(username="user1", password_hash="hashed456", role="user"),
        ]

        session.add_all(questions + users)
        await session.commit()

    print("Seed completed.")


if __name__ == "__main__":
    asyncio.run(seed())
