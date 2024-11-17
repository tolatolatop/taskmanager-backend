from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from datetime import datetime
from pydantic import ValidationError

router = APIRouter()

@router.get("/instances", response_model=List[schemas.Instance])
def get_instances(db: Session = Depends(database.get_db)):
    return db.query(models.Instance).all()

@router.post("/instances", response_model=schemas.Instance, status_code=201)
def create_instance(instance: schemas.InstanceBase, db: Session = Depends(database.get_db)):
    try:
        instance_data = instance.model_dump(by_alias=False)
        db_instance = models.Instance(**instance_data)
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
        return db_instance
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": "数据验证错误", "errors": e.errors()}
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"message": f"创建实例失败: {str(e)}"}
        )

@router.get("/instances/{instance_id}", response_model=schemas.Instance)
def get_instance(instance_id: int, db: Session = Depends(database.get_db)):
    instance = db.query(models.Instance).filter(models.Instance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="实例不存在")
    return instance

@router.put("/instances/{instance_id}/status")
def update_instance_status(
    instance_id: int, 
    status: str,
    db: Session = Depends(database.get_db)
):
    try:
        instance = db.query(models.Instance).filter(models.Instance.id == instance_id).first()
        if instance is None:
            raise HTTPException(status_code=404, detail="实例不存在")
        
        # 验证状态是否合法
        if status not in ["running", "stopped", "maintenance"]:
            raise HTTPException(status_code=400, detail="无效的状态值")
        
        instance.status = status
        instance.last_heartbeat = datetime.now()
        
        db.commit()
        db.refresh(instance)
        
        return {
            "status": instance.status,
            "lastHeartbeat": instance.last_heartbeat
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"message": f"更新实例状态失败: {str(e)}"}
        )

@router.get("/instances/{instance_id}/status")
def get_instance_status(instance_id: int, db: Session = Depends(database.get_db)):
    instance = db.query(models.Instance).filter(models.Instance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="实例不存在")
    return {
        "status": instance.status,
        "lastHeartbeat": instance.last_heartbeat
    }

# 批量创建实例的接口
@router.post("/instances/batch", response_model=List[schemas.Instance])
def create_instances_batch(instances: List[schemas.InstanceBase], db: Session = Depends(database.get_db)):
    try:
        db_instances = []
        for instance in instances:
            instance_data = instance.model_dump(by_alias=False)
            db_instance = models.Instance(**instance_data)
            db.add(db_instance)
            db_instances.append(db_instance)
        
        db.commit()
        for instance in db_instances:
            db.refresh(instance)
            
        return db_instances
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={"message": "数据验证错误", "errors": e.errors()}
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={"message": f"批量创建实例失败: {str(e)}"}
        )