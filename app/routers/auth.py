from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth_schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, RefreshTokenRequest, TokenResponse
from app.services import auth_service

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    result = auth_service.handle_register(req, db)
    
    if result == auth_service.FOUND_USER:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tài khoản email đã tồn tại"
        )
    
    return RegisterResponse(message="Đăng ký tài khoản thành công", email=req.email)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def login(request: Request, req: LoginRequest, db: Session = Depends(get_db)):
    err_message, access_token, refresh_token = auth_service.handle_login(req, db)
    
    if err_message == auth_service.NOT_FOUND_USER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email không tồn tại"
        )
    if err_message == auth_service.INCORRECT_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu không chính xác"
        )
    if err_message == auth_service.ACCOUNT_LOCKED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đang bị khóa"
        )
    return LoginResponse(
        message="Đăng nhập thành công",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh_token(req: RefreshTokenRequest, db: Session = Depends(get_db)):
    new_token, err = auth_service.handle_refresh_token(req.refresh_token, db)
    if err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err)
    return TokenResponse(access_token=new_token)