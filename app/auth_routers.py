from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db
from app.schemas import UserCreate, Token
from app.auth import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


auth_router = APIRouter()

blacklisted_tokens = set()

@auth_router.post("/logout")
def logout(request: Request, token: str = Depends(oauth2_scheme)):
    blacklisted_tokens.add(token)
    return {"message": "Logged out successfully"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token has been revoked")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


@auth_router.post(path='/register', response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter_by(email=user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"user_id": new_user.id})
    return {"access_token": token, "token_type": "bearer"}

@auth_router.post(path="/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }