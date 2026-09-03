from sqlalchemy.orm import Session
from app.models import ResearchProjectModel, ResearchMemberModel, UserModel, ResearchTaskModel
from app.schemas.project_schemas import ProjectCreateRequest, ProjectUpdateRequest, MemberAddRequest

NOT_FOUND_PROJECT = "Không tìm thấy đề tài nghiên cứu"
FORBIDDEN_PROJECT = "Bạn không có quyền truy cập đề tài này"
MEMBER_ALREADY_EXISTS = "Thành viên đã tồn tại trong đề tài"
NOT_FOUND_USER = "Người dùng không tồn tại"
CANNOT_REMOVE_LAST_OWNER = "Không thể xóa Owner duy nhất"

def handle_create_project(req: ProjectCreateRequest, user_id: int, db: Session):
    new_project = ResearchProjectModel(
        name=req.name,
        description=req.description,
        owner_id=user_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    owner_member = ResearchMemberModel(
        project_id=new_project.id,
        user_id=user_id,
        role="OWNER"
    )
    db.add(owner_member)
    db.commit()
    return new_project

def handle_get_user_projects(user_id: int, db: Session, search: str = None):
    query = db.query(ResearchProjectModel).join(ResearchMemberModel).filter(
        ResearchMemberModel.user_id == user_id
    )
    if search:
        query = query.filter(ResearchProjectModel.name.ilike(f"%{search}%"))
    return query.all()

def handle_get_project_detail(project_id: int, user_id: int, db: Session):
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first()
    if not project:
        return NOT_FOUND_PROJECT

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_PROJECT

    return project

def handle_update_project(project_id: int, req: ProjectUpdateRequest, user_id: int, db: Session):
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first()
    if not project:
        return NOT_FOUND_PROJECT

    if project.owner_id != user_id:
        return FORBIDDEN_PROJECT

    if req.name is not None:
        project.name = req.name
    if req.description is not None:
        project.description = req.description

    db.commit()
    db.refresh(project)
    return project

def handle_delete_project(project_id: int, user_id: int, db: Session):
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first()
    if not project:
        return NOT_FOUND_PROJECT

    if project.owner_id != user_id:
        return FORBIDDEN_PROJECT

    db.delete(project)
    db.commit()
    return True

def handle_add_member(project_id: int, req: MemberAddRequest, user_id: int, db: Session):
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first()
    if not project:
        return NOT_FOUND_PROJECT

    if project.owner_id != user_id:
        return FORBIDDEN_PROJECT

    target_user = db.query(UserModel).filter(UserModel.id == req.user_id).first()
    if not target_user:
        return NOT_FOUND_USER

    existing = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == req.user_id
    ).first()
    if existing:
        return MEMBER_ALREADY_EXISTS

    new_member = ResearchMemberModel(
        project_id=project_id,
        user_id=req.user_id,
        role=req.role
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def handle_get_members(project_id: int, user_id: int, db: Session):
    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == user_id
    ).first()
    if not member:
        return FORBIDDEN_PROJECT

    return db.query(ResearchMemberModel).filter(ResearchMemberModel.project_id == project_id).all()

def handle_remove_member(project_id: int, target_user_id: int, user_id: int, db: Session):
    project = db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first()
    if not project:
        return NOT_FOUND_PROJECT

    if project.owner_id != user_id:
        return FORBIDDEN_PROJECT

    if target_user_id == project.owner_id:
        return CANNOT_REMOVE_LAST_OWNER

    member = db.query(ResearchMemberModel).filter(
        ResearchMemberModel.project_id == project_id,
        ResearchMemberModel.user_id == target_user_id
    ).first()
    if not member:
        return NOT_FOUND_USER

    db.query(ResearchTaskModel).filter(
        ResearchTaskModel.project_id == project_id,
        ResearchTaskModel.assignee_id == target_user_id
    ).update({"assignee_id": None})

    db.delete(member)
    db.commit()
    return True
