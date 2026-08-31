from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schemas import UserResponse
from app.models.user import UserModel
from app.dependencies.auth_deps import get_current_user, RoleCheck
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[UserResponse])
def get_all_users(
    search_name: Optional[str] = Query(None, description="Tìm kiếm theo tên"),
    search_email: Optional[str] = Query(None, description="Tìm kiếm theo email"),
    is_active: Optional[bool] = Query(None, description="Lọc theo trạng thái hoạt động"),
    current_user: UserModel = Depends(RoleCheck(["ADMIN"])),
    db: Session = Depends(get_db)
):
    return user_service.get_users_list(db, search_name=search_name,search_email=search_email, is_active=is_active)