from fastapi import APIRouter
from app.major.dao import MajorDAO
from app.major.schemas import SMajorAdd

router = APIRouter(prefix='/majors', tags=['Работа с факультетами'])


@router.post('/add/', summary='Добавить факультет')
async def get_major(major: SMajorAdd) -> dict:
    check = await MajorDAO.add(**major.model_dump())
    if check:
        return {'msg': 'Факультет успешно добавлен!', 'major': major}
    else:
        return {'msg': 'Ошибка при добавлении факультета.'}
