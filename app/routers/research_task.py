from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from typing import List, Optional
from app.schemas.task_schemas import TaskResponse, TaskCreateRequest, TaskAssignRequest, TaskUpdateRequest
from app.services import task_service, auth_service

task_router = APIRouter(prefix="/research-tasks", tags=["Research Tasks"])

def get_user_id(user_info: dict) -> int:
    if isinstance(user_info, dict):
        return user_info.get("user_id")
    return getattr(user_info, "id", None)

@task_router.post("/{project_id}/research-tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(project_id: int, req: TaskCreateRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = task_service.handle_create_task(project_id=project_id, req=req, user_id=user_id, db=db)
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ thành viên đề tài mới được tạo nhiệm vụ")
    if data == task_service.INVALID_ASSIGNEE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee phải là thành viên trong đề tài")
    return data

@task_router.patch("/research-tasks/{task_id}/assign", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def assign_task(task_id: int, req: TaskAssignRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = task_service.handle_assign_task(task_id=task_id, req=req, user_id=user_id, db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền giao việc")
    if data == task_service.INVALID_ASSIGNEE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee phải là thành viên trong đề tài")
    return data

@task_router.get("/{project_id}/research-tasks", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
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

@task_router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_detail(task_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = task_service.handle_get_task_detail(task_id=task_id, user_id=user_id, db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xem nhiệm vụ này")
    return data

@task_router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int, 
    req: TaskUpdateRequest, 
    user_info: dict = Depends(auth_service.handle_get_user), 
    db: Session = Depends(get_db)
):
    user_id = get_user_id(user_info)
    data = task_service.handle_update_task(task_id=task_id, req=req, user_id=user_id, db=db)
    
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
        
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền chỉnh sửa nhiệm vụ này (Chỉ người được gán việc mới được thay đổi trạng thái)"
        )
        
    if data == task_service.INVALID_ASSIGNEE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee phải là thành viên trong đề tài")
        
    return data

@task_router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    user_id = get_user_id(user_info)
    data = task_service.handle_delete_task(task_id=task_id, user_id=user_id, db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xóa nhiệm vụ này")
    return {"message": "Xóa nhiệm vụ thành công"}