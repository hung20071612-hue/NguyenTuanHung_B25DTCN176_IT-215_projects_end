from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth_schemas import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services import auth_service

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

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    result, token = auth_service.handle_login(req, db)
    if result == auth_service.NOT_FOUND_USER:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email không tồn tại"
        )
    if result == auth_service.INCORRECT_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu không chính xác"
        )
    if result == auth_service.ACCOUNT_LOCKED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đang bị khóa"
        )
    
    return LoginResponse(
        message="Đăng nhập thành công",
        access_token=token,
        token_type="bearer"
    )