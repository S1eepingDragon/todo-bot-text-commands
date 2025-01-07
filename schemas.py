from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., example="Купить молоко")
    description: Optional[str] = Field(None, example="2 литра свежего молока")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Купить хлеб")
    description: Optional[str] = Field(None, example="Цельнозерновой")
    completed: Optional[bool] = Field(None, example=True)


class TaskResponse(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True