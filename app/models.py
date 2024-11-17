from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

# 创建任务和实例的多对多关系表
task_instance = Table('task_instance', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('instance_id', Integer, ForeignKey('instances.id'))
)

class TaskStatus(str, enum.Enum):
    PENDING = "待处理"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    FAILED = "失败"

class TaskType(str, enum.Enum):
    NORMAL = "normal"
    DEPLOY = "deploy"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    type = Column(String)
    status = Column(String, default=TaskStatus.PENDING)
    progress = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    
    instances = relationship("Instance", secondary=task_instance, backref="tasks")
    logs = relationship("TaskLog", backref="task")

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    timestamp = Column(DateTime, default=datetime.now)
    message = Column(String)

class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ip = Column(String)
    region = Column(String)
    status = Column(String)
    specification = Column(String)
    cpu_type = Column(String, name="cpuType")
    last_heartbeat = Column(DateTime, name="lastHeartbeat") 