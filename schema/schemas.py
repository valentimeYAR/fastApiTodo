from typing import TypeVar, Generic

from pydantic import BaseModel, Field


def todo_serializer(todo) -> dict:
    return {
        "id": str(todo.get("_id", "")),  # ✅ Преобразуем ObjectId в строку
        "title": todo.get("title", ""),
        "description": todo.get("description", ""),
        "completed": todo.get("completed", False),
    }

def todos_serializer(todos) -> list:
    return [todo_serializer(todo) for todo in todos]

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    message: str = Field(..., description='Иформация по ответу', examples=['<INFO>'])
    data: T

    @classmethod
    def success(cls, data: T):
        return cls(message="Успешно", data=data)