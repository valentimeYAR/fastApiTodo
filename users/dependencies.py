from datetime import datetime, timezone, timedelta

from bson import ObjectId
from fastapi import HTTPException, Cookie, status, Request
from jose import JWTError
from jose import jwt
from passlib.context import CryptContext

from config.api import get_auth_data
from config.database import users_collection
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_access_token(token: str):
    """
    Декодирует JWT-токен и возвращает его данные.
    """
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        return payload  # Декодированный токен (словарь)
    except JWTError:
        return None  # Если токен недействителен

# Принимает пароль, возвращает безопасный хеш
def get_password_hash(password: str) -> str:
    return password_context.hash(password)


# Принимает пароль и хешированный пароль и возвращает результат проверки
def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def get_current_user(request: Request):
    token = request.cookies.get('user_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден"
        )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")

        user = users_collection.find_one({"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

        return user  # Возвращаем данные пользователя

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")


def get_current_user_role(request: Request):
    token = request.cookies.get('user_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден"
        )
    try:
        payload = decode_access_token(token)
        print(payload)
        role = payload.get("role")
        if not role or role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Невалидный токен или нет доступа")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен")

    return True
