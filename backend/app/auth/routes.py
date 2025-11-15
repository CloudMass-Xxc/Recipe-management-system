from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.auth.password import get_password_hash, verify_password, generate_user_id
from app.auth.jwt import create_access_token
from app.auth.exceptions import UserAlreadyExistsException, IncorrectPasswordException, UserNotFoundException
from app.auth.dependencies import get_current_user
from app.auth.schemas import UserCreate, UserLogin, Token, UserInfo, UserUpdate, PasswordUpdate, Message

router = APIRouter(prefix="/auth", tags=["认证"])

# 用户注册
@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise UserAlreadyExistsException(detail="用户名已存在")
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_data.email).first():
        raise UserAlreadyExistsException(detail="邮箱已被注册")
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        user_id=generate_user_id(),
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        display_name=user_data.display_name,
        diet_preferences=user_data.diet_preferences
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# 用户登录
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录接口（支持OAuth2密码流）
    """
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise IncorrectPasswordException(detail="用户名或密码错误")
    
    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        raise IncorrectPasswordException(detail="用户名或密码错误")
    
    # 检查用户是否活跃
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户信息
@router.get("/me", response_model=UserInfo)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    return current_user

# 更新用户信息
@router.put("/me", response_model=UserInfo)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息
    """
    # 更新用户信息
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

# 更新密码
@router.put("/change-password", response_model=Message)
async def change_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户密码
    """
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise IncorrectPasswordException(detail="旧密码错误")
    
    # 更新密码
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "密码更新成功", "success": True}