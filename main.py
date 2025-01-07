from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from database import SessionLocal, engine, get_db
from schemas import TaskCreate, TaskUpdate, TaskResponse
from crud import create_task, get_tasks, get_task_by_id, update_task, delete_task
from models import Base

app = FastAPI()

if not os.path.exists("./data/app.db"):
    print("База данных не обнаружена. Запуск инициализации...")
    from init_db import init_db
    init_db()
    print("База данных успешно инициализирована.")


@app.post("/tasks", response_model=TaskResponse)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@app.get("/tasks", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db=db)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}
