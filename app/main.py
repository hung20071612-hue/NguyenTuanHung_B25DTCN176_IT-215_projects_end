from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.database import engine, Base
from app.routers import auth, users, research_project, research_task
from app.core.exceptions import global_exception_handler

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(research_project.project_router)
app.include_router(research_task.task_router)

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "Research Group Management API is running"}