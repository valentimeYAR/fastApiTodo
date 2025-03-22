from fastapi import APIRouter, HTTPException, Response, Depends
from starlette import status

from config.database import users_collection
from schema.schemas import BaseResponse
from users.dependencies import get_password_hash, verify_password, create_access_token, get_current_user
from users.schemas import UserLoginSchema, UserRegisterSchema, UserData, UserLoginResponse

router = APIRouter()


@router.post('/login', response_model=BaseResponse[UserLoginResponse], summary='Вход пользователя')
def login(response: Response, user_data: UserLoginSchema):
    user = users_collection.find_one({'login': user_data.login})

    if not user or verify_password(password=user_data.password, hashed_password=user['password']) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль"
        )

    access_token = create_access_token({
        "sub": str(user['_id']),
        "role": str(user['role']),
    })

    response.set_cookie(
        key="user_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return BaseResponse.success(data={'accessToken': access_token, 'refreshToken': "refresh_token"})


@router.post('/register', response_model=BaseResponse[UserData], summary='Регистрация пользователя')
def register(user_data: UserRegisterSchema):
    user = users_collection.find_one({'login': user_data.login})
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Пользователь уже существует')
    user_dict = dict(user_data)
    user_dict['password'] = get_password_hash(user_data.password)
    result = users_collection.insert_one(dict(user_dict))
    if result.inserted_id:
        return BaseResponse.success(UserData(
            login=user_dict['login'],
            name=user_dict['name'],
            lastName=user_dict['lastName'],
        ))

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail='Пользователь уже существует')
