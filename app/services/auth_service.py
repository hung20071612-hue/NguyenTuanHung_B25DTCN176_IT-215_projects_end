from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from app.db.database import get_db
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
    refresh_token = security.create_refresh_token(user_id=user.id)

    return None, access_token, refresh_token

security_token = HTTPBearer()

def handle_get_user(
    cre: HTTPAuthorizationCredentials = Depends(security_token),
    db: Session = Depends(get_db)
):
    token = cre.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ")
        user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản không tồn tại")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị khóa")
        return {
            "user_id": user.id,
            "username": user.email,
            "role_name": user.role
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token đã hết hạn, vui lòng đăng nhập lại")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ")

def handle_refresh_token(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            return None, "Token không hợp lệ"
        
        user_id = int(payload.get("sub"))
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user or not user.is_active:
            return None, "Tài khoản không khả dụng"

        new_access_token = security.create_access_token(
            user_id=user.id,
            username=user.email,
            role_user=user.role
        )
        return new_access_token, None
    except jwt.ExpiredSignatureError:
        return None, "Refresh token đã hết hạn"
    except jwt.PyJWTError:
        return None, "Token không hợp lệ"