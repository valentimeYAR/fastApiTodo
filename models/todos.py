from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    id: Optional[str] = Field(None, description="Уникальный ID в MongoDB", examples=['Айди туду'])
    title: str = Field(..., description="Название задачи", examples=['Название туду'])
    description: str = Field(..., description="Описание задачи", examples=['Описание туду'])
    completed: bool = Field(False, description="Статус выполнения", examples=[True])

    class Config:
        schema_extra = {
            "example": {
                "id": "65d4f3e27a8b9e56c4f4b2e1",
                "title": "Купить продукты",
                "description": "Магазин пятерочка",
                "completed": False
            }
        }
