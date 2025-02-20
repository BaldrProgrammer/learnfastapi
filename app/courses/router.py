from fastapi import APIRouter
from app.courses.schemas import SCourse, SCourseAdd
from app.courses.dao import CourseDAO

router = APIRouter(prefix='/courses', tags=['Работа с курсами'])

@router.get('/', summary='Получить все курсы')
async def get_all_courses() -> list[SCourse]:
    return await CourseDAO.find_all()


@router.post('/add/', summary='Добавить курс')
async def add_course(course: SCourseAdd) -> dict:
    print('1111111111111111111111111111\n', course.model_dump())
    check = await CourseDAO.add(**course.model_dump())
    if check:
        return {'msg': 'Курс успешно добавлен.', 'course_id': check.id}
    else:
        return {'msg': 'Ошибка при удалении курса'}
