from app.dao.base import BaseDAO
from app.students.models import Major

class MajorDAO(BaseDAO):
    model = Major
