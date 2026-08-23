from sqlalchemy.orm import Session
from app.models import ResearchTaskModel, ResearchMemberModel
from app.schemas.task_schemas import TaskCreateRequest, TaskUpdateRequest

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

    if req.assignee_id:
        assignee_member = db.query(ResearchMemberModel).filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == req.assignee_id
        ).first()
        if not assignee_member:
            return INVALID_ASSIGNEE

    new_task = ResearchTaskModel(
        project_id=project_id,
        title=req.title,
        description=req.description,
        assignee_id=req.assignee_id,
        priority=req.priority,
        due_date=req.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

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

    # Mandatory Sorting
    sort_column = getattr(ResearchTaskModel, sort_by, ResearchTaskModel.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Mandatory Pagination
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

    if req.assignee_id:
        assignee_member = db.query(ResearchMemberModel).filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == req.assignee_id
        ).first()
        if not assignee_member:
            return INVALID_ASSIGNEE
        task.assignee_id = req.assignee_id

    if req.title is not None:
        task.title = req.title
    if req.description is not None:
        task.description = req.description
    if req.status is not None:
        task.status = req.status
    if req.priority is not None:
        task.priority = req.priority
    if req.due_date is not None:
        task.due_date = req.due_date

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

    db.delete(task)
    db.commit()
    return True
