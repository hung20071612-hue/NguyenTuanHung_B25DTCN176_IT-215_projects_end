from sqlalchemy.orm import Session
from app.models import ResearchTaskModel, ResearchMemberModel, ResearchProjectModel
from app.schemas.task_schemas import TaskCreateRequest, TaskAssignRequest, TaskUpdateStatus, TaskUpdateRequest

NOT_FOUND_TASK = "Không tìm thấy nhiệm vụ nghiên cứu"
FORBIDDEN_TASK = "Bạn không có quyền thao tác trên nhiệm vụ này"
INVALID_ASSIGNEE = "Assignee phải là thành viên trong đề tài"

def handle_create_task(project_id: int, req: TaskCreateRequest, user_id: int, db: Session):
    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK

    new_task = ResearchTaskModel(
        project_id=project_id,
        title=req.title,
        description=req.description,
        assignee_id=None,
        priority=req.priority,
        due_date=req.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def handle_assign_task(task_id: int, req: TaskAssignRequest, db: Session):
    task = db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first()
    if not task:
        return NOT_FOUND_TASK 

    is_member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == task.project_id,
        ResearchMemberModel.user_id == req.assignee_id
    ).first()

    if not is_member:
        return INVALID_ASSIGNEE

    task.assignee_id = req.assignee_id
    db.commit()
    db.refresh(task)
    return task

def handle_get_tasks(project_id: int, user_id: int, db: Session, status: str = None, priority: str = None, search: str = None, limit: int = 10, offset: int = 0, sort_by: str = "created_at", sort_order: str = "desc"):
    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK

    query = db.query(ResearchTaskModel).filter(ResearchTaskModel.project_id == project_id)
    if status:
        query = query.filter(ResearchTaskModel.status == status)
    if priority:
        query = query.filter(ResearchTaskModel.priority == priority)
    if search:
        query = query.filter(ResearchTaskModel.title.ilike(f"%{search}%"))

    sort_column = getattr(ResearchTaskModel, sort_by, ResearchTaskModel.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.offset(offset).limit(limit).all()

def handle_get_task_detail(task_id: int, user_id: int, db: Session):
    task = db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first()
    if not task:
        return NOT_FOUND_TASK

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == task.project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK

    return task

def handle_update_task_status(task_id: int, req: TaskUpdateStatus, user_id: int, db: Session):
    task = db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first()
    if not task:
        return NOT_FOUND_TASK

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == task.project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK

    update_data = req.model_dump(exclude_unset=True) 
    
    if "status" in update_data:
        if task.assignee_id is None or task.assignee_id != user_id:
            return FORBIDDEN_TASK

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def handle_update_task(task_id: int, req: TaskUpdateRequest, user_id: int, db: Session):
    task = db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first()
    if not task:
        return NOT_FOUND_TASK

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == task.project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK
 
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == task.project_id).first()
    is_owner = (project.owner_id == user_id)
    if not is_owner:
            return FORBIDDEN_TASK

    update_data = req.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

def handle_delete_task(task_id: int, user_id: int, db: Session):
    task = db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first()
    if not task:
        return NOT_FOUND_TASK

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == task.project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_TASK

    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == task.project_id).first()

    is_owner = (project.owner_id == user_id)

    if not is_owner:
        return FORBIDDEN_TASK

    db.delete(task)
    db.commit()
    return True
