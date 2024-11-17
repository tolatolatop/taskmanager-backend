from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from datetime import datetime
from pydantic import ValidationError

router = APIRouter()

@router.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    try:
        task_data = task.model_dump()
        instance_ids = [instance['id'] for instance in task_data.pop('instances', [])]
        
        db_task = models.Task(**task_data)
        
        if instance_ids:
            instances = db.query(models.Instance).filter(
                models.Instance.id.in_(instance_ids)
            ).all()
            
            found_ids = {instance.id for instance in instances}
            missing_ids = set(instance_ids) - found_ids
            if missing_ids:
                raise HTTPException(
                    status_code=400,
                    detail=f"实例ID不存在: {missing_ids}"
                )
            
            db_task.instances = instances
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
        
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": "数据验证错误", "errors": e.errors()}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"message": f"创建任务失败: {str(e)}"}
        )

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    try:
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task is None:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        update_data = task.model_dump(exclude_unset=True)
        
        if 'instances' in update_data:
            instance_ids = [instance['id'] for instance in update_data.pop('instances')]
            instances = db.query(models.Instance).filter(
                models.Instance.id.in_(instance_ids)
            ).all()
            
            found_ids = {instance.id for instance in instances}
            missing_ids = set(instance_ids) - found_ids
            if missing_ids:
                raise HTTPException(
                    status_code=400,
                    detail=f"实例ID不存在: {missing_ids}"
                )
            
            db_task.instances = instances
        
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
        
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": "数据验证错误", "errors": e.errors()}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"message": f"更新任务失败: {str(e)}"}
        )

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None

@router.get("/tasks/{task_id}/logs", response_model=List[schemas.TaskLog])
def get_task_logs(task_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.TaskLog).filter(models.TaskLog.task_id == task_id).all() 