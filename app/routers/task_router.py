from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schemas import TaskUpdateRequest, TaskResponse
from app.services import task_service, auth_service

task_router = APIRouter(prefix="/research-tasks", tags=["Research Tasks"])

@task_router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_detail(task_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    data = task_service.handle_get_task_detail(task_id=task_id, user_id=user_info["user_id"], db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xem nhiệm vụ này")
    return data

@task_router.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, req: TaskUpdateRequest, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    data = task_service.handle_update_task(task_id=task_id, req=req, user_id=user_info["user_id"], db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền chỉnh sửa nhiệm vụ này")
    if data == task_service.INVALID_ASSIGNEE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee phải là thành viên trong đề tài")
    return data

@task_router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, user_info: dict = Depends(auth_service.handle_get_user), db: Session = Depends(get_db)):
    data = task_service.handle_delete_task(task_id=task_id, user_id=user_info["user_id"], db=db)
    if data == task_service.NOT_FOUND_TASK:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nhiệm vụ không tồn tại")
    if data == task_service.FORBIDDEN_TASK:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền xóa nhiệm vụ này")
    return {"message": "Xóa nhiệm vụ thành công"}
