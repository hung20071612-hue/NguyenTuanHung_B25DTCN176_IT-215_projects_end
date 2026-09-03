# seed.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.user import UserModel, UserRole
from app.models.research_project import ResearchProjectModel, ResearchMemberModel, MemberRole
from app.models.research_task import ResearchTaskModel, TaskStatus, TaskPriority
from app.core.security import handle_hash_password

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # 1. Seed Users
        admin_user = db.query(UserModel).filter(UserModel.email == "admin@gmail.com").first()
        if not admin_user:
            admin_user = UserModel(
                email="admin@gmail.com",
                password_hash=handle_hash_password("admin123"),
                full_name="Administrator System",
                role=UserRole.ADMIN
            )
            db.add(admin_user)

        user1 = db.query(UserModel).filter(UserModel.email == "owner@gmail.com").first()
        if not user1:
            user1 = UserModel(
                email="owner@gmail.com",
                password_hash=handle_hash_password("user1234"),
                full_name="Nguyễn Văn Chủ Đề Tài",
                role=UserRole.USER
            )
            db.add(user1)

        user2 = db.query(UserModel).filter(UserModel.email == "member@gmail.com").first()
        if not user2:
            user2 = UserModel(
                email="member@gmail.com",
                password_hash=handle_hash_password("user1234"),
                full_name="Trần Thị Thành Viên",
                role=UserRole.USER
            )
            db.add(user2)

        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        # 2. Seed Project
        project = db.query(ResearchProjectModel).filter(ResearchProjectModel.name == "Nghiên cứu ứng dụng AI vào Y tế").first()
        if not project:
            project = ResearchProjectModel(
                name="Nghiên cứu ứng dụng AI vào Y tế",
                description="Đề tài cấp Trường về chẩn đoán ảnh X-quang",
                owner_id=user1.id
            )
            db.add(project)
            db.commit()
            db.refresh(project)

            # Add members
            m1 = ResearchMemberModel(project_id=project.id, user_id=user1.id, role=MemberRole.OWNER)
            m2 = ResearchMemberModel(project_id=project.id, user_id=user2.id, role=MemberRole.MEMBER)
            db.add_all([m1, m2])
            db.commit()

            # 3. Seed Tasks
            task1 = ResearchTaskModel(
                project_id=project.id,
                title="Thu thập Dataset ảnh X-quang",
                description="Tải dữ liệu từ Kaggle và làm sạch",
                assignee_id=user2.id,
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.HIGH
            )
            task2 = ResearchTaskModel(
                project_id=project.id,
                title="Huấn luyện mô hình ResNet50",
                description="Chạy bài toán phân loại trên GPU",
                assignee_id=user1.id,
                status=TaskStatus.TODO,
                priority=TaskPriority.MEDIUM
            )
            db.add_all([task1, task2])
            db.commit()

        print("--- SEED DỮ LIỆU MẪU THÀNH CÔNG ---")
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()