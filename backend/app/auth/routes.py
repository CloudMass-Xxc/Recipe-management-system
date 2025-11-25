from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user
from app.core.utils import generate_unique_id
from app.auth.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    LoginResponse
)

router = APIRouter(prefix="/auth", tags=["认证"])


# 用户注册
@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    """
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查手机号是否已存在
    if user_data.phone and db.query(User).filter(User.phone == user_data.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )
    
    # 创建密码哈希
    hashed_password = get_password_hash(user_data.password)
    
    # 创建新用户
    db_user = User(
        user_id=generate_unique_id(),  # 生成唯一用户ID
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        display_name=user_data.display_name,
        password_hash=hashed_password,
        is_active='Y',  # 使用字符串'Y'/'N'，符合数据库模型设计
        is_superuser=False,
        created_at=datetime.utcnow()
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 生成访问令牌
    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            user_id=str(db_user.user_id),
            username=db_user.username,
            email=db_user.email,
            phone=db_user.phone,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    }

# 用户登录
@router.post("/login", response_model=LoginResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口（支持手机号/邮箱/用户名）
    """
    identifier = login_data.identifier.strip()
    
    # 查找用户
    user: Optional[User] = None
    if identifier.isdigit():
        user = db.query(User).filter(User.phone == identifier).first()
    if user is None and "@" in identifier:
        user = db.query(User).filter(User.email == identifier).first()
    if user is None:
        user = db.query(User).filter(User.username == identifier).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 检查用户是否活跃
    if user.is_active != 'Y':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用"
        )
    
    # 生成访问令牌
    access_token = create_access_token(data={"sub": str(user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            user_id=str(user.user_id),
            username=user.username,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    }

# 获取当前用户信息
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    return UserResponse(
        user_id=str(current_user.user_id),
        username=current_user.username,
        email=current_user.email,
        phone=current_user.phone,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

# 用户退出登录
@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    用户退出登录接口
    
    注意：由于使用JWT认证，主要的退出登录逻辑在客户端（清除token）。
    此端点提供后端支持，可用于实现更复杂的退出逻辑（如token黑名单等）。
    """
    return {"message": "退出登录成功"}