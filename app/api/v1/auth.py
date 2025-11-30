from fastapi import APIRouter, Depends, HTTPException, status, Form , Request
from sqlalchemy.orm import Session
from app.core.CRUD import create_user , update_user
from app.middleware.rate_limit import limiter
# Dependancy
from app.api.deps import get_db , get_current_user , role_required

# DATA MODEL
from app.models.user import User
from app.models.post import Post

# SECURITY
from app.core.security import hash_password, verify_password

from fastapi.responses import JSONResponse

from app.schemas.user import UserBase, UserLogin, PostBase, UserUpdate
from app.services.auth_service import create_access_token , create_refresh_token , decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register')
async def register(user: UserBase, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create user directly
    hash_pwd = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hash_pwd, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "success"}

@router.post('/login')
@limiter.limit("5/minute")
async def login(user: UserLogin, request: Request, db: Session = Depends(get_db)):
    user_email = db.query(User).filter(User.email == user.email).first()
    if not user_email:
        raise HTTPException(status_code=400, detail="Email does not exist")

    if not verify_password(user.password, user_email.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    #Set session
    request.session["user_id"] = user_email.id

    access_token = create_access_token({"sub": str(user_email.id) , "type":"access"})
    refresh_token = create_refresh_token({"sub": str(user_email.id) , "type":"refresh"})
    response = JSONResponse(status_code=201, content={"message": "Login successful"})
    response.set_cookie("access_token", access_token, httponly=True,samesite="lax")
    response.set_cookie("refresh_token", refresh_token, httponly=True,samesite="lax")
    return response

@router.post('/post_upload')
async def post_upload(post: PostBase, request: Request, db: Session = Depends(get_db)):
    current = get_current_user(request,db)
    new_post = Post(title=post.title, content=post.content, author=current.username)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    response = JSONResponse(status_code=201, content={"message": "Upload successful"})
    return response

@router.get('/get-post')
async def get_posts(request:Request ,db: Session = Depends(get_db)):
    current = get_current_user(request,db)
    post = db.query(Post).filter(Post.author == current.username).all()
    return post if post else []

@router.get('/feed')
async def get_feed(request:Request ,db: Session = Depends(get_db)):
    current = get_current_user(request,db)
    posts = db.query(Post).order_by(Post.id.desc()).all()
    return posts

@router.get('/post/{id}')
async def get_post( request:Request,id: int, db: Session = Depends(get_db)):
    current = get_current_user(request,db)
    get_post_specific = db.query(Post).filter(Post.id == id, Post.author == current.username).first()
    if not get_post_specific:
        raise HTTPException(status_code=404, detail="Post not found")
    response = {"post": get_post_specific}
    return response

@router.delete('/post/{id}')
async def delete_post(id: int, request: Request, db: Session = Depends(get_db)):
    current = get_current_user(request, db)
    post = db.query(Post).filter(Post.id == id, Post.author == current.username).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    response = JSONResponse(status_code=204, content={"message": "Post deleted"})
    return response

@router.post("/admin/update/{user_name}")
async def admin_panel(
    user_name: str,
    request: Request,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin = Depends(role_required("admin"))
):
    # Find target user by username
    target_user = db.query(User).filter(User.username == user_name).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields directly
    if user_update.username:
        target_user.username = user_update.username
    if user_update.email:
        target_user.email = user_update.email
    if user_update.password:
        target_user.hashed_password = hash_password(user_update.password)
    if user_update.role:
        if admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can update roles")
        target_user.role = user_update.role
    
    db.commit()
    db.refresh(target_user)
    
    updated = {
        "message": "update success",
        "user": {
            "id": target_user.id,
            "username": target_user.username,
            "email": target_user.email,
            "role": target_user.role
        }
    }

    return {
        "message": "User updated successfully",
        "updated": updated
    }



BLACK_LIST_TOKEN = set()
BLACK_LIST_RETOKEN = set()

@router.get('/admin/users')
async def get_all_users(request: Request, db: Session = Depends(get_db), admin = Depends(role_required("admin"))):
    users = db.query(User).all()
    return [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    } for user in users]

@router.get('/admin/user/{user_name}')
async def get_userinfo(user_name: str, request: Request, db: Session = Depends(get_db), admin = Depends(role_required("admin"))):
    target_user = db.query(User).filter(User.username == user_name).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": target_user.id,
        "username": target_user.username,
        "email": target_user.email,
        "role": target_user.role
    }


@router.post('/logout')
async def logout(request:Request, db: Session = Depends(get_db)):
    get_access_token = request.cookies.get("access_token")
    if not get_access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    BLACK_LIST_TOKEN.add(get_access_token)
    get_refresh_token = request.cookies.get("refresh_token")
    if not get_refresh_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    BLACK_LIST_RETOKEN.add(get_refresh_token)
    response = JSONResponse(status_code=200, content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response