# RESEARCH GROUP MANAGEMENT API - MANDATORY TASKS ONLY

Dự án đã được tinh chỉnh chỉ giữ lại đúng và đủ các **Task Bắt Buộc** (65 điểm) theo file bảng điểm `Project_FastAPI_research.xlsx`. All optional/bonus features (Comments, Attachments, Refresh Token, Seed script) đã được loại bỏ hoàn toàn.

## Cấu trúc thư mục:
```
research_management/
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── core/
    │   ├── __init__.py
    │   ├── config.py
    │   └── security.py
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   ├── research_project.py
    │   └── research_task.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── auth_schemas.py
    │   ├── user_schemas.py
    │   ├── project_schemas.py
    │   └── task_schemas.py
    ├── services/
    │   ├── __init__.py
    │   ├── auth_service.py
    │   ├── user_service.py
    │   ├── project_service.py
    │   └── task_service.py
    └── routers/
        ├── __init__.py
        ├── auth_router.py
        ├── user_router.py
        ├── project_router.py
        └── task_router.py
```

## Khởi chạy:
```bash
uvicorn app.main:app --reload
```
