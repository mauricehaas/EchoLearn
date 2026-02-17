from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select
from typing import List

from app.core.db import get_session
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


# Alle User abrufen
@router.get("/")
async def get_users() -> List[User]:
    """Defines the GET Endpoint for retrieving all users
    
    Returns:
        List[User]: A list of all users in the database
    """
    async for session in get_session():
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


# Einen User nach ID abrufen
@router.get("/{user_id}")
async def get_user(user_id: int) -> User:
    """Defines the GET Endpoint for retrieving a user by their ID
    
    Args:
        user_id (int): The ID of the user to retrieve
        
    Raises:
        HTTPException: If no user with the given ID is found, an HTTPException with status
        code 404 is raised.
    
    Returns:
        User: The user object with the specified ID
    """
    async for session in get_session():
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
