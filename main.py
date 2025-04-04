import uvicorn
from fastapi import FastAPI

from routes.route import router
from users.router import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4200"],  # Можно указать ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix='/todos', tags=["Todos"])
app.include_router(user_router, prefix='/user', tags=["User"])





if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# .venv\Scripts\activate