from fastapi import Request, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from app.services.auth_service import decode_token
from app.core.database import SessionLocal

from app.models.user import User


# DB DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    return user

def role_required(role: str):
    def check(request: Request, db: Session = Depends(get_db)):
        current_user = get_current_user(request, db)
        if current_user.role != role:
            raise HTTPException(status_code=403, detail="Admin Can Only Access")
        return current_user
    return check