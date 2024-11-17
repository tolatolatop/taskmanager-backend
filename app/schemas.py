from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# 先定义 Instance 相关的模型
class InstanceBase(BaseModel):
    name: str
    ip: str
    region: str
    status: str = Field(default="running")
    specification: str
    cpu_type: str = Field(alias="cpuType")
    last_heartbeat: Optional[datetime] = Field(default_factory=datetime.now, alias="lastHeartbeat")

    class Config:
        populate_by_name = True

class Instance(InstanceBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class InstanceStatusUpdate(BaseModel):
    status: str

class InstanceCreate(InstanceBase):
    class Config:
        populate_by_name = True

class InstanceUpdate(BaseModel):
    name: Optional[str] = None
    ip: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    specification: Optional[str] = None
    cpu_type: Optional[str] = Field(None, alias="cpuType")

    class Config:
        populate_by_name = True

# 然后定义 Task 相关的模型
class TaskInstanceData(BaseModel):
    id: int
    name: str
    ip: str
    region: str
    status: str
    specification: str
    cpuType: str
    lastHeartbeat: Optional[str] = None

class TaskBase(BaseModel):
    title: str
    description: str
    type: str
    instances: List[TaskInstanceData] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    type: Optional[str] = None
    instances: Optional[List[TaskInstanceData]] = None

class Task(BaseModel):
    id: int
    title: str
    description: str
    type: str
    status: str
    progress: float
    created_at: datetime = Field(alias="createdAt")
    completed_at: Optional[datetime] = Field(None, alias="completedAt")
    instances: List[Instance] = []

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class TaskLog(BaseModel):
    timestamp: datetime
    message: str

class InstanceBase(BaseModel):
    name: str
    ip: str
    region: str
    status: str = Field(default="running")
    specification: str
    cpu_type: str = Field(alias="cpuType")
    last_heartbeat: Optional[datetime] = Field(default_factory=datetime.now, alias="lastHeartbeat")

    class Config:
        populate_by_name = True

class Instance(InstanceBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True

class InstanceStatusUpdate(BaseModel):
    status: str

class InstanceCreate(InstanceBase):
    class Config:
        populate_by_name = True

class InstanceUpdate(BaseModel):
    name: Optional[str] = None
    ip: Optional[str] = None
    region: Optional[str] = None
    status: Optional[str] = None
    specification: Optional[str] = None
    cpu_type: Optional[str] = Field(None, alias="cpuType")

    class Config:
        populate_by_name = True 