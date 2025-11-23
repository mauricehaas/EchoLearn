from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from app.core.db import get_session
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


# Alle User abrufen
@router.get("/")
async def get_users():
    async for session in get_session():
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


# Einen User nach ID abrufen
@router.get("/{user_id}")
async def get_user(user_id: int):
    async for session in get_session():
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
