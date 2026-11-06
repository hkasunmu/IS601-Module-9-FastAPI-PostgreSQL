
import os
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Base, User
from app.schemas import UserCreate, UserRead
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@lru_cache
def get_engine():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

    engine = create_engine(database_url, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    return engine


def get_session():
    with Session(get_engine()) as session:
        yield session


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    new_user = User(
        username=user_data.username,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
    )

    session.add(new_user)

    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        ) from exc

    session.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
