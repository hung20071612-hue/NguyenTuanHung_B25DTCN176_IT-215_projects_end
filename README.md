
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

