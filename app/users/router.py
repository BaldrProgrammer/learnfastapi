from fastapi import APIRouter, HTTPException, status
from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister

router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.post('/register/', summary='Создание пользователя')
async def register(user: SUserRegister) -> dict:
    current_user = await UsersDAO.find_one_or_none_by_filter(email=user.email)
    if current_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует.'
        )
    user_dict = user.model_dump()
    user_dict['password'] = get_password_hash(user.password)
    await UsersDAO.add(**user_dict)
    return {'msg': 'Пользователь успешно создан.'}
