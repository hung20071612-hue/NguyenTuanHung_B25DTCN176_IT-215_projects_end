from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.project_schemas import (
    ProjectCreateRequest, ProjectUpdateRequest, ProjectResponse,
    MemberAddRequest, MemberResponse
)
from app.schemas.task_schemas import TaskCreateRequest, TaskResponse
from app.services import project_service, task_service, auth_service

project_router = APIRouter(prefix="/research-projects", tags=["Research Projects"])

def get_user_id(user_info: dict) -> int:
    if isinstance(user_info, dict):
        return user_info.get("user_id")
    return getattr(user_info, "id", None)

@project_router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(req: ProjectCreateRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    return project_service.handle_create_project(req=req, user_id=user_id, db=db)

@project_router.get("", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
def get_my_projects(search: Optional[str] = None, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    return project_service.handle_get_user_projects(user_id=user_id, db=db, search=search)

@project_router.get("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def get_project_detail(project_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = project_service.handle_get_project_detail(project_id=project_id, user_id=user_id, db=db)
    if data == project_service.NOT_FOUND_PROJECT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đề tài không tồn tại")
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền truy cập đề tài")
    return data

@project_router.patch("/{project_id}", response_model=ProjectResponse, status_code=status.HTTP_200_OK)
def update_project(project_id: int, req: ProjectUpdateRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = project_service.handle_update_project(project_id=project_id, req=req, user_id=user_id, db=db)
    if data == project_service.NOT_FOUND_PROJECT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đề tài không tồn tại")
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền chỉnh sửa")
    return data

@project_router.delete("/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(project_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = project_service.handle_delete_project(project_id=project_id, user_id=user_id, db=db)
    if data == project_service.NOT_FOUND_PROJECT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đề tài không tồn tại")
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền xóa")
    return {"message": "Xóa đề tài thành công"}

@project_router.post("/{project_id}/members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def add_member(project_id: int, req: MemberAddRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = project_service.handle_add_member(project_id=project_id, req=req, user_id=user_id, db=db)
    if data == project_service.NOT_FOUND_PROJECT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đề tài không tồn tại")
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới được thêm thành viên")
    if data == project_service.NOT_FOUND_USER:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User thêm không tồn tại")
    if data == project_service.MEMBER_ALREADY_EXISTS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Thành viên đã ở trong đề tài")
    return data

@project_router.get("/{project_id}/members", response_model=List[MemberResponse], status_code=status.HTTP_200_OK)
def get_members(project_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = project_service.handle_get_members(project_id=project_id, user_id=user_id, db=db)
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xem thành viên")
    return data

@project_router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_200_OK)
def remove_member(project_id: int, user_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    current_user_id = get_user_id(user_info)
    data = project_service.handle_remove_member(project_id=project_id, target_user_id=user_id, user_id=current_user_id, db=db)
    if data == project_service.NOT_FOUND_PROJECT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Đề tài không tồn tại")
    if data == project_service.FORBIDDEN_PROJECT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới được xóa thành viên")
    if data == project_service.CANNOT_REMOVE_LAST_OWNER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa OWNER duy nhất")
    if data == project_service.NOT_FOUND_USER:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không thuộc đề tài")
    return {"message": "Xóa thành viên khỏi đề tài thành công"}

@project_router.post("/{project_id}/research-tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, req: TaskCreateRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = task_service.handle_create_task(project_id=project_id, req=req, user_id=user_id, db=db)
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ thành viên đề tài mới được tạo nhiệm vụ")
    if data == task_service.INVALID_ASSIGNEE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee phải là thành viên trong đề tài")
    return data

@project_router.get("/{project_id}/research-tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(
    project_id: int, 
    status_filter: Optional[str] = None, 
    priority: Optional[str] = None, 
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    user_info: dict = Depends(auth_service.handle_get_user), 
    db: Session = Depends(get_db)
):
    user_id = get_user_id(user_info)
    data = task_service.handle_get_tasks(
        project_id=project_id, 
        user_id=user_id, 
        db=db, 
        status=status_filter, 
        priority=priority, 
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xem nhiệm vụ")
    return data