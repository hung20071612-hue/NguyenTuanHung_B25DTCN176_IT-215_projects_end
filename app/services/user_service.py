from sqlalchemy.orm import Session
from app.models.user import UserModel

def handle_get_me(user_id: int, db: Session):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users_list(db: Session, search_name: str = None,search_email: str = None , is_active: bool = None):
    query = db.query(UserModel)
    if search_name:
        query = query.filter((UserModel.full_name.ilike(f"%{search_name}%")))
    if search_email:
        query = query.filter((UserModel.email.ilike(f"%{search_email}%")))
    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)
    return query.all()