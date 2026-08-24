from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from app.models.user import UserModel
from app.schemas.auth_schemas import RegisterRequest, LoginRequest
from app.core import security
from app.core.config import settings

FOUND_USER = "Tài khoản email đã tồn tại"
NOT_FOUND_USER = "Email không tồn tại"
INCORRECT_PASSWORD = "Mật khẩu không chính xác"
ACCOUNT_LOCKED = "Tài khoản đang bị khóa"

def handle_register(req: RegisterRequest, db: Session):
    user = db.query(UserModel).filter(UserModel.email == req.email).first()
    if user:
        return FOUND_USER

    hashed_password = security.handle_hash_password(req.password)
    new_account = UserModel(
        email=req.email,
        password_hash=hashed_password,
        full_name=req.full_name,
        role="USER"
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

def handle_login(req: LoginRequest, db: Session):
    user = db.query(UserModel).filter(UserModel.email == req.email).first()
    if not user:
        return NOT_FOUND_USER, None

    if not user.is_active:
        return ACCOUNT_LOCKED, None

    is_valid_password = security.check_password(req.password, user.password_hash)
    if not is_valid_password:
        return INCORRECT_PASSWORD, None

    access_token = security.create_access_token(
        user_id=user.id,
        username=user.email,
        role_user=user.role
    )

    return None, access_token

security_token = HTTPBearer()

def handle_get_user(cre: HTTPAuthorizationCredentials = Depends(security_token)):
    token = cre.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
            "role_name": payload.get("role_user")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn, vui lòng đăng nhập lại"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ"
        )