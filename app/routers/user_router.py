from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.user_schemas import UserResponse
from app.services import user_service, auth_service
from app.services.auth_service import RoleCheck

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    return user_service.handle_get_me(user_id=user_info["user_id"], db=db)

@user_router.get("", response_model=List[UserResponse], dependencies=[Depends(RoleCheck(["Admin"]))], status_code=status.HTTP_200_OK)
def get_all_users(search: Optional[str] = None, db: Session = Depends(get_db)):
    return user_service.handle_get_all_users(db=db, search=search)
