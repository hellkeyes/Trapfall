from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.auth.security import hash_password, verify_password
from backend.app.auth.schemas import RegisterRequest, UserResponse, LoginRequest
from backend.app.auth.jwt import create_access_token
from backend.app.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post('/register', response_model=UserResponse)
def register(register_request: RegisterRequest, db: Session = Depends(get_db)):

    query = select(User).where(
        or_(
            User.email == register_request.email,
            User.username == register_request.username
        )
    )

    existing_user = db.execute(query).scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=409, detail="This email or username already exists")


    new_user = User(
        username = register_request.username,
        email = register_request.email,
        password_hash = hash_password(register_request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post('/login')
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    query = select(User).where(User.email == login_request.email)
    existing_user = db.execute(query).scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code=401, detail="User doesn't exist. Please register first")

    password_valid = verify_password(login_request.password, existing_user.password_hash)


    if not password_valid:
        raise HTTPException(status_code=401, detail="Username or email is wrong")

    access_token = create_access_token({'user_id': existing_user.id})

    return {
    "access_token": access_token,
    "token_type": "bearer"
    }

