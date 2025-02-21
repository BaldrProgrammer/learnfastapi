from fastapi import APIRouter
from app.students.schemas import SStudent
from app.courses.schemas import SCourse, SCourseAdd, SCourseUpd
from app.courses.dao import CourseDAO

router = APIRouter(prefix='/courses', tags=['Работа с курсами'])


@router.get('/', summary='Получить все курсы')
async def get_all_courses() -> list[SCourse]:
    return await CourseDAO.find_all()


@router.get('/students/{course_id}', summary='Получить всех студентов курса')
async def get_all_course_students(course_id: int) -> list[SStudent]:
    course = await CourseDAO.find_one_or_none_by_id(course_id)
    return course.students


@router.post('/add/', summary='Добавить курс')
async def add_course(course: SCourseAdd) -> dict:
    check = await CourseDAO.add(**course.model_dump())
    if check:
        return {'msg': 'Курс успешно добавлен', 'course_id': check.id}
    else:
        return {'msg': 'Ошибка при удалении курса'}


@router.patch('/update/', summary='Обновить курс')
async def update_course(course_id: int, new_info: SCourseUpd) -> dict:
    check = await CourseDAO.update_course(course_id, new_info.model_dump())
    if check:
        return {'msg': 'Курс успешно обновлён'}
    else:
        return {'msg': 'Ошибка при обновлении курса'}


@router.delete('/delete/{course_id}', summary='Удалить курс')
async def delete_course(course_id: int) -> dict:
    check = await CourseDAO.delete(id=course_id)
    if check:
        return {'msg': 'Курс успешно удалён', 'rowcount': check}
    else:
        return {'msg': 'Ошибка при удалении курса'}
