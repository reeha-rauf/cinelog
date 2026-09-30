from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_db
from app.auth.models import User, Follow
from app.auth.schemas import UserCreate, UserResponse, Token, FollowResponse, FollowerResponse
from app.auth.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_current_user(request: Request, token: str = Depends(oauth2_scheme_optional), db: Session = Depends(get_db)):
    if not token:
        token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user




@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db.refresh(new_user)
    return new_user



@router.post("/login", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=1800,
    )
    return {"access_token": token, "token_type": "bearer"}



@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.post("/follow/{user_id}", response_model=FollowResponse)
def follow_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    follow = Follow(follower_id=current_user.id, followed_id=user_id)
    db.add(follow)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already following this user")
    db.refresh(follow)
    return follow

@router.delete("/unfollow/{user_id}", status_code=204)
def unfollow_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == user_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")
    db.delete(follow)
    db.commit()

@router.get("/followers/{user_id}", response_model=List[FollowerResponse])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = (
        db.query(User)
        .join(Follow, Follow.follower_id == User.id)
        .filter(Follow.followed_id == user_id)
        .all()
    )
    return followers

@router.get("/following/{user_id}", response_model=List[FollowerResponse])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = (
        db.query(User)
        .join(Follow, Follow.followed_id == User.id)
        .filter(Follow.follower_id == user_id)
        .all()
    )
    return following