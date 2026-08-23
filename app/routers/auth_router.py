from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services import auth_service

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    data = auth_service.handle_register(req=req, db=db)
    if data == auth_service.FOUND_USER:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tài khoản email đã tồn tại")
    return {"message": "Đăng ký thành công", "email": data.email}

@auth_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    data = auth_service.handle_login(req=req, db=db)
    if data == auth_service.NOT_FOUND_USER:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tài khoản không tồn tại")
    if data == auth_service.ACCOUNT_LOCKED:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị khóa")
    if data == auth_service.INCORRECT_PASSWORD:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu không chính xác")
    return data
