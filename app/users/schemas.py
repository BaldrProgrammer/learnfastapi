from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description='Электронная почта')
    password: str = Field(..., description='Пароль')
    phone_number: str = Field(..., description='Номер телефона')
    first_name: str = Field(..., description='Имя')
    last_name: str = Field(..., description='Фамилия')

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value
