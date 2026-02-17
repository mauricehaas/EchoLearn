from sqlalchemy import Column, Integer, String

from app.core.db import Base


class User(Base):
    """Database Schema for Table Users

    Attributes:
        id (int): primary key of the table
        username (str): the username for the user
        password_hash (str): the encoded password that belongs to this user
        role (str): determines the permissions of the user within the system, either user or admin, default user
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
