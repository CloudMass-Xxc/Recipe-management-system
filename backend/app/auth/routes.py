from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
import logging
import traceback
from uuid import UUID
from sqlalchemy import or_

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.auth.schemas import UserCreate, UserLogin, UserResponse, TokenResponse, RegisterResponse, LoginResponse
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import create_access_token, get_current_user
from app.auth.dependencies import get_current_active_user

# 创建路由器
router = APIRouter(prefix="/auth", tags=["auth"])

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 添加文件处理器
file_handler = logging.FileHandler("auth.log")
file_handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 添加处理器到日志记录器
if not logger.handlers:
    logger.addHandler(file_handler)


@router.post("/register", response_model=RegisterResponse, summary="用户注册")
async def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    - **username**: 用户名（3-50个字符）
    - **email**: 电子邮箱（必须是有效的邮箱格式）
    - **phone**: 手机号码（可选，格式必须正确且唯一）
    - **password**: 密码（至少6位字符）
    
    返回用户注册成功信息
    """
    client_ip = request.client.host
    logger.info(f"收到注册请求 - 用户名: {user_data.username}, 邮箱: {user_data.email}, IP: {client_ip}")
    
    try:
        logger.info(f"注册数据完整信息 - username: {user_data.username}, email: {user_data.email}, phone: {user_data.phone}")
        
        # 构建查询条件
        filters = []
        if user_data.username:
            filters.append(User.username == user_data.username)
            logger.info(f"添加用户名过滤条件: {user_data.username}")
        if user_data.email:
            filters.append(User.email == user_data.email)
            logger.info(f"添加邮箱过滤条件: {user_data.email}")
        if user_data.phone:
            filters.append(User.phone == user_data.phone)
            logger.info(f"添加手机号过滤条件: {user_data.phone}")
        
        logger.info(f"最终过滤条件列表: {filters}")
        
        # 如果有任何过滤条件，执行查询
        existing_user = None
        if filters:
            logger.info("执行数据库查询，检查用户是否已存在...")
            existing_user = db.query(User).filter(or_(*filters)).first()
            logger.info(f"查询结果 - existing_user: {existing_user}")
            if existing_user:
                logger.info(f"找到现有用户 - ID: {existing_user.user_id}, username: {existing_user.username}, email: {existing_user.email}, phone: {existing_user.phone}")
            else:
                logger.info("没有找到现有用户")
        
        if existing_user:
            if existing_user.username == user_data.username:
                logger.warning(f"注册失败 - 用户名已存在: {user_data.username}, IP: {client_ip}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="用户名已存在"
                )
            elif existing_user.email == user_data.email:
                logger.warning(f"注册失败 - 邮箱已被注册: {user_data.email}, IP: {client_ip}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
            elif user_data.phone and existing_user.phone == user_data.phone:
                logger.warning(f"注册失败 - 手机号已被注册: {user_data.phone}, IP: {client_ip}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号已被注册"
                )
        
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_password,
            display_name=user_data.username,  # 默认使用用户名作为显示名
            is_active='Y'  # 默认激活用户
        )
        
        # 保存到数据库
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"用户注册成功: {user_data.username}, 用户ID: {new_user.user_id}, IP: {client_ip}")
        
        # 构建响应
        user_response = UserResponse(
            user_id=str(new_user.user_id),
            username=new_user.username,
            email=new_user.email,
            phone=new_user.phone,
            is_active=new_user.is_active == 'Y'
        )
        
        return RegisterResponse(
            message="注册成功",
            success=True,
            data=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}, 用户名: {user_data.username}, IP: {client_ip}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册过程中发生错误"
        )


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    用户登录接口
    
    - **username**: 用户名、邮箱或手机号
    - **password**: 密码
    
    返回登录成功信息和访问令牌
    """
    client_ip = request.client.host
    identifier = login_data.username  # 支持用户名、邮箱或手机号登录
    logger.info(f"收到登录请求 - 标识符: {identifier}, IP: {client_ip}")
    
    try:
        # 查找用户 - 支持用户名、邮箱或手机号登录
        user = db.query(User).filter(
            (User.username == identifier) | 
            (User.email == identifier) | 
            (User.phone == identifier)
        ).first()
        
        if not user:
            logger.warning(f"登录失败 - 用户不存在: {identifier}, IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 检查用户是否被锁定
        if user.locked_until:
            logger.warning(f"登录失败 - 用户已被锁定: {identifier}, IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账户已被锁定，请稍后再试"
            )
        
        # 验证密码
        if not verify_password(login_data.password, user.password_hash):
            # 增加登录失败次数
            user.failed_login_attempts += 1
            logger.warning(f"登录失败 - 密码错误, 失败次数: {user.failed_login_attempts}, 标识符: {identifier}, IP: {client_ip}")
            
            # 如果失败次数达到限制，可以在这里添加锁定逻辑
            if user.failed_login_attempts >= 5:
                logger.warning(f"登录失败 - 密码错误次数过多，账户将被锁定: {identifier}, IP: {client_ip}")
                # 这里可以添加锁定逻辑，例如设置锁定时间
            
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        
        # 检查用户是否激活
        if user.is_active != 'Y':
            logger.warning(f"登录失败 - 用户已被停用: {identifier}, IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户已被停用"
            )
        
        # 重置登录失败次数
        user.failed_login_attempts = 0
        db.commit()
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"用户登录成功: {user.username}, 用户ID: {user.user_id}, IP: {client_ip}")
        
        # 构建用户响应
        user_response = UserResponse(
            user_id=str(user.user_id),
            username=user.username,
            email=user.email,
            phone=user.phone,
            is_active=user.is_active == 'Y'
        )
        
        # 构建令牌响应
        token_response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
        return LoginResponse(
            message="登录成功",
            success=True,
            data=token_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}, 用户名: {login_data.username}, IP: {client_ip}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登录过程中发生错误"
        )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户的信息
    
    需要在请求头中携带有效的Bearer令牌
    
    返回当前用户的详细信息
    """
    client_ip = request.client.host
    logger.info(f"收到获取用户信息请求 - 用户ID: {current_user.user_id}, IP: {client_ip}")
    
    try:
        user_response = UserResponse(
            user_id=str(current_user.user_id),
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
            is_active=current_user.is_active == 'Y'
        )
        
        logger.info(f"获取用户信息成功 - 用户ID: {current_user.user_id}, IP: {client_ip}")
        return user_response
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}, 用户ID: {current_user.user_id}, IP: {client_ip}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )
