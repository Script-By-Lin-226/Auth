from sqlalchemy.orm import Session
from fastapi import Depends, Request, HTTPException
from app.models.user import User
from app.core.security import verify_password, hash_password
from app.schemas.user import UserBase , UserUpdate
from app.api.deps import get_db, get_current_user

#CREATE USER
def create_user(user: UserBase,db: Session = Depends(get_db)):
    hash_pwd = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hash_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "success"}

def update_user(
    request: Request,
    user: UserUpdate,
    db: Session = Depends(get_db)
):

    current_user = get_current_user(request, db)
    
    # Check if admin is updating another user
    if hasattr(request.state, 'target_user'):
        exist = request.state.target_user
    else:
        exist = db.query(User).filter(User.username == current_user.username).first()
    
    if not exist:
        raise HTTPException(status_code=404, detail="User not found")

    # Update username
    if user.username:
        exist.username = user.username

    # Update email
    if user.email:
        exist.email = user.email

    # Update password
    if user.password:
        exist.hashed_password = hash_password(user.password)

    # Update role (only admin)
    if user.role:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can update roles")
        exist.role = user.role

    db.commit()
    db.refresh(exist)

    return {"message": "update success", "user": {
        "id": exist.id,
        "username": exist.username,
        "email": exist.email,
        "role": exist.role
    }}