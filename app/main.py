from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse

from app.routers.auth_router import auth_router
from app.routers.user_router import user_router
from app.routers.project_router import project_router
from app.routers.task_router import task_router
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.status_code,
            "message": exc.detail
        }
    )


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
