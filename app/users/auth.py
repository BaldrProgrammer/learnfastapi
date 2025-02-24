from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from pydantic import EmailStr
from app.config import get_auth_data
from app.users.dao import UsersDAO
from app.users.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_date = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire_date})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none_by_filter(email=email)
    if not user or not verify_password(password=password, hash_password=user.password):
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не найден'
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь на найден')

    return user


async def get_admin_user(user_data: User = Depends(get_current_user)):
    if user_data.is_admin:
        return user_data
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Недостаточно прав!'
    )
