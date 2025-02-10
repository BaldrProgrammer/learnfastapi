from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent


router = APIRouter(prefix='/students', tags=['Работа со студентами'])

@router.get('/', summary='получить всех студентов')
async def get_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())


@router.get('/{id}', summary='получить одного студента по id')
async def get_student_by_id(student_id: int) -> SStudent | dict:
    student = await StudentDAO.find_full_data(student_id)
    if student:
        return student
    else:
        return {'msg': 'Пользователя с таким id нет!'}


@router.get('/by_filter', summary='получить одного студента по фильтрам')
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | dict:
    student = await StudentDAO.find_one_or_none_by_filter(**request_body.to_dict())
    if student:
        return student
    else:
        return {'msg': 'Пользователя с таким id нет!'}
