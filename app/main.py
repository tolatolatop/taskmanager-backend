from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import tasks, instances

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="任务管理系统")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(instances.router, prefix="/api", tags=["instances"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用任务管理系统 API"} 