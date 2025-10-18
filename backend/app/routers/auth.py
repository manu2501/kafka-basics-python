from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..auth import create_access_token, get_password_hash, verify_password
from ..database import get_db
from ..models import User, UserRole

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        role=UserRole.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(str(user.id), user.role.value)
    return schemas.TokenResponse(access_token=token)
