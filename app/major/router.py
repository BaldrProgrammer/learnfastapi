from fastapi import APIRouter
from app.major.dao import MajorDAO
from app.major.schemas import SMajor, SMajorAdd, SMajorUpdDesc

router = APIRouter(prefix='/majors', tags=['Работа с факультетами'])


@router.get('/', summary='Получить список факультетов')
async def get_majors() -> list[SMajor]:
    return await MajorDAO.find_all()


@router.post('/add/', summary='Добавить факультет')
async def add_major(major: SMajorAdd) -> dict:
    check = await MajorDAO.add(**major.model_dump())
    if check:
        return {'msg': 'Факультет успешно добавлен!', 'major': major}
    else:
        return {'msg': 'Ошибка при добавлении факультета.'}


@router.put('/update_description/', summary='Обновить факультет')
async def update_major(major: SMajorUpdDesc) -> dict:
    check = await MajorDAO.update(
        filter_by={'major_name': major.major_name},
        major_description=major.major_description
    )
    if check:
        return {'msg': 'Факультет успешно обновлен.', 'major': major, 'rowcount': check}
    else:
        return {'msg': 'Обновление факультета не удалось.'}


@router.delete('/delete/{major_id}', summary='Удалить факультет')
async def delete_major(major_id: int) -> dict:
    check = await MajorDAO.delete(id=major_id)
    if check:
        return {'msg': 'Успешно удален факультет.', 'major_id': major_id, 'rowcount': check}
    else:
        return {'msg': 'Ошибка при удалении факультета.'}
