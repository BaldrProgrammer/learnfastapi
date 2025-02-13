from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent


router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get('/', summary='получить всех студентов')
async def get_students() -> list[SStudent]:
    return await StudentDAO.find_all()


@router.get('/{id}', summary='получить одного студента по id')
async def get_student_by_id(student_id: int) -> SStudent | dict:
    student = await StudentDAO.find_full_data(student_id)
    if student:
        return student
    else:
        return {'msg': 'Пользователя с таким id нет!'}


@router.get('/filter_by', summary='получить всех студентов по фильтрам')
async def get_students_by_filter(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(True, **request_body.to_dict())
