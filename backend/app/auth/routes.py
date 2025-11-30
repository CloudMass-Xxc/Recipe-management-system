from datetime import timedelta, datetime
from typing import Any, Dict, Optional
import uuid
import logging

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    refresh_access_token as refresh_token,
    blacklist_token,
    verify_token
)
from app.auth.dependencies import get_current_user
from app.auth.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    LoginResponse,
    TokenRefresh
)
from app.core.config import settings

# 配置日志记录器
logger = logging.getLogger(__name__)

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
    
    # 创建新用户（使用带日志记录的方法）
    db_user = User(
        user_id=uuid.uuid4(),  # 生成唯一用户ID，返回UUID对象
        username=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        display_name=user_data.display_name or user_data.username,  # 如果没有提供display_name，默认使用username
        password_hash=hashed_password,
        is_active='Y',  # 使用字符串'Y'/'N'，符合数据库模型设计
        is_superuser=False,
        created_at=datetime.utcnow()
    )
    
    db_user = db_user.save(db)
    
    # 记录用户注册
    logger.info(f"New user registered: {db_user.username} (ID: {db_user.user_id})")
    
    # 生成访问令牌和刷新令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.user_id)},
        expires_delta=access_token_expires
    )
    refresh_token_str = create_refresh_token(data={"sub": str(db_user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token_str,
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
def login(request: Request, login_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录接口（支持手机号/邮箱/用户名）
    """
    identifier = login_data.identifier.strip()
    
    # 记录登录请求信息
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent", "Unknown")
    logger.info(f"Login attempt from IP: {client_ip}, User-Agent: {user_agent}, Identifier: {identifier}")
    
    # 查找用户（使用带日志记录的方法）
    user: Optional[User] = None
    
    # 按优先级查找：先尝试手机号，再尝试邮箱，最后尝试用户名
    # 注意：这里移除了isdigit()检查，因为手机号格式可能包含非数字字符（如国家代码、分隔符等）
    # 让数据库查询来处理具体的匹配逻辑
    logger.debug(f"[DEBUG] Attempting phone lookup for: '{identifier}'")
    user = User.get_by_phone(db, identifier)
    if user:
        logger.debug(f"[DEBUG] Found user by phone: {user.username} (ID: {user.user_id})")
    else:
        logger.debug(f"[DEBUG] No user found by phone: '{identifier}'")
    
    # 如果不是手机号或没找到，尝试邮箱
    if user is None and "@" in identifier:
        logger.debug(f"[DEBUG] Attempting email lookup for: '{identifier}'")
        user = User.get_by_email(db, identifier)
        if user:
            logger.debug(f"[DEBUG] Found user by email: {user.username} (ID: {user.user_id})")
        else:
            logger.debug(f"[DEBUG] No user found by email: '{identifier}'")
    
    # 如果都不是，尝试用户名
    if user is None:
        logger.debug(f"[DEBUG] Attempting username lookup for: '{identifier}'")
        user = User.get_by_username(db, identifier)
        if user:
            logger.debug(f"[DEBUG] Found user by username: {user.username} (ID: {user.user_id})")
        else:
            logger.debug(f"[DEBUG] No user found by username: '{identifier}'")
    
    if not user:
        logger.warning(f"Login failed: User not found - {identifier}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.password_hash):
        logger.warning(f"Login failed: Invalid password for user - {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 检查用户是否活跃
    if user.is_active != 'Y':
        logger.warning(f"Login failed: Disabled account attempt - {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用"
        )
    
    # 生成访问令牌和刷新令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires
    )
    refresh_token_str = create_refresh_token(data={"sub": str(user.user_id)})
    
    logger.info(f"Login successful: {user.username} (ID: {user.user_id})")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token_str,
        "user": UserResponse(
            user_id=str(user.user_id),
            username=user.username,
            email=user.email,
            phone=user.phone,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    }

# 刷新访问令牌
@router.post("/refresh", response_model=LoginResponse)
def refresh(request: Request, token_in: TokenRefresh, db: Session = Depends(get_db)):
    """
    刷新访问令牌接口
    """
    # 记录刷新令牌请求
    client_ip = request.client.host
    logger.info(f"Token refresh attempt from IP: {client_ip}")
    
    try:
        # 调用增强后的刷新令牌函数
        tokens = refresh_token(token_in.refresh_token, request, db)
        
        # 获取用户ID
        payload = verify_token(token_in.refresh_token)
        if not payload or "sub" not in payload:
            logger.warning("Token refresh failed: Invalid token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        user_id = payload["sub"]
        
        # 从数据库获取用户（使用带日志记录的方法）
        user = User.get_by_id(db, user_id)
        if not user:
            logger.warning("Token refresh failed: User not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        logger.info(f"Token refresh successful for user: {user.username} (ID: {user.user_id})")
        
        return {
            "access_token": tokens["access_token"],
            "token_type": "bearer",
            "refresh_token": tokens["refresh_token"],
            "user": UserResponse(
                user_id=str(user.user_id),
                username=user.username,
                email=user.email,
                phone=user.phone,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        }
        
    except HTTPException as e:
        logger.error(f"Token refresh failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="刷新令牌时发生错误"
        )

# 获取当前用户信息
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    
    注意：所有用户数据均直接从数据库读取，确保数据真实性和安全性。
    """
    logger.info(f"User data access: {current_user.username} (ID: {current_user.user_id}) - Requesting own profile")
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
def logout(request: Request, current_user: User = Depends(get_current_user)):
    """
    用户退出登录接口
    
    实现令牌撤销机制，将当前使用的访问令牌添加到黑名单
    """
    # 从请求头获取访问令牌
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]  # 移除 "Bearer " 前缀
        
        # 将令牌添加到黑名单
        blacklist_token(token)
        logger.info(f"User logged out: {current_user.username} (ID: {current_user.user_id}) - Token blacklisted")
    else:
        logger.warning(f"Logout attempt without valid token for user: {current_user.username}")
    
    return {"message": "退出登录成功，所有会话已终止"}