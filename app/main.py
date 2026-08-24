from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import auth, users, research_project, research_task
from app.core.exceptions import global_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(research_project.project_router)
app.include_router(research_task.task_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "Research Group Management API is running"}