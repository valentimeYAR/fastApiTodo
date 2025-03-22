import re

from pydantic import BaseModel, Field, field_validator


class UserLoginSchema(BaseModel):
    login: str = Field(..., description='Login пользователя', examples=['<LOGIN>'])
    password: str = Field(..., description='Пароль пользователя', examples=['<PASSWORD>'])

class UserLoginResponse(BaseModel):
    accessToken: str = Field(..., description='Token пользователя', examples=['<TOKEN>'])
    refreshToken: str = Field(..., description='RefreshToken пользователя', examples=['<RefreshToken>'])\


    class Config:
        schema_extra = {
            "example": {
                "accessToken": "<accessToken>",
                "refreshToken": "<refreshToken>",
            }
        }


class UserRegisterSchema(BaseModel):
    login: str = Field(..., description='Login пользователя', examples=['<LOGIN>'])
    password: str = Field(..., description='Пароль пользователя', examples=['<PASSWORD>'])
    name: str = Field(..., description='Имя пользователя', examples=['<NAME>'])
    lastName: str = Field(..., description='Фамилия пользователя', examples=['<LASTNAME>'])
    role: str = Field(default='user', description='Роль пользователя', exclude=True)

    @field_validator('login')
    def validate_login(cls, v):
        print(v)
        if len(v) <= 3:
            raise ValueError('Длинна логина должна быть больше 3-х символов')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not re.fullmatch(r'[A-Za-z]+', v):
            raise ValueError('Пароль должен содержать буквы A-Z')
        return v

class UserData(BaseModel):
    login: str = Field(..., description='Login пользователя', examples=['<LOGIN>'])
    name: str = Field(..., description='Имя пользователя', examples=['<NAME>'])
    lastName: str = Field(..., description='Фамилия пользователя', examples=['<LASTNAME>'])
