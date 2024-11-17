import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from . import models
from abc import ABC, abstractmethod
from typing import Optional

class TaskLogger:
    """任务日志记录器"""
    def __init__(self, db: Session, task_id: int):
        self.db = db
        self.task_id = task_id

    def info(self, message: str):
        """记录信息日志"""
        self._log(f"[INFO] Task-{self.task_id} - {message}")

    def error(self, message: str):
        """记录错误日志"""
        self._log(f"[ERROR] Task-{self.task_id} - {message}")

    def debug(self, message: str):
        """记录调试日志"""
        self._log(f"[DEBUG] Task-{self.task_id} - {message}")

    def _log(self, message: str):
        """写入日志到数据库"""
        log = models.TaskLog(
            task_id=self.task_id,
            message=message,
            timestamp=datetime.now()
        )
        self.db.add(log)
        self.db.commit()

class TaskManager:
    """任务状态管理器"""
    def __init__(self, db: Session, task_id: int):
        self.db = db
        self.task_id = task_id

    def update_progress(self, progress: float, status: Optional[str] = None):
        """更新任务进度和状态"""
        task = self._get_task()
        if task:
            task.progress = progress
            if status:
                task.status = status
            self.db.commit()

    def complete_task(self):
        """完成任务"""
        task = self._get_task()
        if task:
            task.status = models.TaskStatus.COMPLETED
            task.progress = 100
            task.completed_at = datetime.now()
            self.db.commit()

    def fail_task(self):
        """标记任务失败"""
        task = self._get_task()
        if task:
            task.status = models.TaskStatus.FAILED
            task.completed_at = datetime.now()
            self.db.commit()

    def _get_task(self):
        """获取任务对象"""
        return self.db.query(models.Task).filter(models.Task.id == self.task_id).first()

class BaseTaskProcessor(ABC):
    """任务处理器基类"""
    def __init__(self, db: Session, task_id: int):
        self.db = db
        self.task_id = task_id
        self.logger = TaskLogger(db, task_id)
        self.manager = TaskManager(db, task_id)

    @abstractmethod
    async def process(self):
        """任务处理主逻辑"""
        pass

    async def execute(self):
        """执行任务并处理异常"""
        try:
            await self.process()
        except Exception as e:
            self.logger.error(f"任务执行失败: {str(e)}")
            self.manager.fail_task()

class TestTaskProcessor(BaseTaskProcessor):
    """测试任务处理器"""
    async def process(self):
        # 等待10秒
        await asyncio.sleep(10)
        
        # 更新进度为50%
        self.manager.update_progress(50, models.TaskStatus.IN_PROGRESS)
        self.logger.info("测试任务进行中，当前进度: 50%")
        
        # 再等待5秒
        await asyncio.sleep(5)
        
        # 完成任务
        self.manager.complete_task()
        self.logger.info("测试任务已完成，进度: 100%")

async def process_test_task(db: Session, task_id: int):
    """任务处理入口函数"""
    processor = TestTaskProcessor(db, task_id)
    await processor.execute()