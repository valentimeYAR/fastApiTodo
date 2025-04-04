from fastapi import APIRouter, HTTPException, Depends

from models.todos import Todo
from config.database import collection
from schema.schemas import todos_serializer
from bson import ObjectId

from users.dependencies import get_current_user, get_current_user_role

router = APIRouter()


# GET request
@router.get('/', response_model=list[Todo], summary='Получение всех туду')
def get_todos():
    todos = todos_serializer(collection.find())
    return todos


@router.post("/create", response_model=Todo, summary="Создание туду")
def create_todo(todo: Todo):
    item = dict(todo)
    result = collection.insert_one(item)

    if result.inserted_id:
        created_todo = collection.find_one({"_id": result.inserted_id})

        return Todo(
            id=str(created_todo["_id"]),
            title=created_todo["title"],
            description=created_todo["description"],
            completed=created_todo["completed"]
        )

    raise HTTPException(status_code=500, detail="Ошибка при создании Todo")


@router.get('/{item_id}', response_model=Todo, summary="Получение одного туду")
def get_todo(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return Todo(
            id=str(item["_id"]),
            title=item["title"],
            description=item["description"],
            completed=item["completed"]
        )
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete('/{item_id}', response_model=dict, summary='Удаление туду')
def delete_todo(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        collection.delete_one({"_id": ObjectId(item_id)})
        return {"success": True}
    raise HTTPException(status_code=404, detail="Item not found")
