from typing import Optional

from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: Optional[str] = Field(None, description="Уникальный ID в MongoDB", examples=['Айди туду'])
    login: str = Field(..., description='Login пользователя', examples=['<LOGIN>'])
    password: str = Field(..., description='Пароль пользователя', examples=['<PASSWORD>'])