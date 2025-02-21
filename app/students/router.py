from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent, SStudentAdd

router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get('/', summary='получить всех студентов')
async def get_students() -> list[SStudent]:
    return await StudentDAO.find_all()


@router.get('/{id}', summary='получить одного студента по id')
async def get_student_by_id(student_id: int) -> SStudent | dict:
    student = await StudentDAO.find_all(True, id=student_id)
    if student:
        return student
    else:
        return {'msg': 'Пользователя с таким id нет!'}


@router.get('/filter_by', summary='получить всех студентов по фильтрам')
async def get_students_by_filter(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(True, **request_body.to_dict())


@router.post('/add/', summary='добавить студента')
async def add_student(student_data: SStudentAdd) -> dict:
    check = await StudentDAO.add_students(student_data.model_dump())
    if check:
        return {'msg': 'Студент успешно добавлен.', 'student': check}
    else:
        return {'msg': 'Ошибка при добавлении студента.'}


@router.patch('/update/', summary='изменить студента')
async def update_student(student_id: int, new_values: dict) -> dict:
    check = await StudentDAO.update_students(student_id, new_values)
    if check:
        return {'msg': 'Студент успешно изменен.', 'new_data': check}
    else:
        return {'msg': 'Ошибка при изменении студента.'}


@router.patch('/change_course/', summary='изменить курс студента')
async def change_course(student_id: int, course_id: int) -> dict:
    check = await StudentDAO.change_course(student_id, course_id)
    if check:
        return {'msg': 'Курс студента успешно изменен.', 'course_id': check}
    else:
        return {'msg': 'Ошибка при изменении курса студента.'}


@router.delete('/delete/{student_id}', summary='удалить студента')
async def delete_student(student_id: int) -> dict:
    check = await StudentDAO.del_students(student_id)
    if check:
        return {'msg': 'Студент успешно удален.', 'deleted_id': check}
    else:
        return {'msg': 'Ошибка при удалении студента.'}
