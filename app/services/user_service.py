from sqlalchemy.orm import Session
from app.models import UserModel

def handle_get_me(user_id: int, db: Session):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def handle_get_all_users(db: Session, search: str = None):
    query = db.query(UserModel)
    if search:
        query = query.filter(
            (UserModel.full_name.ilike(f"%{search}%")) | 
            (UserModel.email.ilike(f"%{search}%"))
        )
    return query.all()
