from fastapi import APIRouter, HTTPException, status, Response, Depends
from app.users.auth import get_password_hash, create_access_token, authenticate_user, get_current_user, get_admin_user
from app.users.models import User
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.get('/me', summary='Получить информацию о залогиненом пользователе')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.get('/all_users/')
async def get_all_users(user_data: User = Depends(get_admin_user)):
    return await UsersDAO.find_all()


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


@router.post('/login/', summary='Аутентификация')
async def login(response: Response, user_data: SUserAuth) -> dict:
    check = await authenticate_user(user_data.email, user_data.password)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль.'
        )
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='access_token', value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.post('/logout/', summary='Выйти из системы')
async def logout(response: Response):
    response.delete_cookie(key='access_token')
    return {'msg': 'Пользователь успешно вышел из системы'}
