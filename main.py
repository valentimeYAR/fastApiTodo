from fastapi import FastAPI

from routes.route import router
from users.router import router as user_router

app = FastAPI()
app.include_router(router, prefix='/todos', tags=["Todos"])
app.include_router(user_router, prefix='/user', tags=["User"])
