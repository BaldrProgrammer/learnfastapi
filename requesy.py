import asyncio

import requests
from app.major.dao import MajorDAO

infos = [
    {
        'major_name': 'Математика',
        'major_description': 'Учим как цифры. Так-же помогает в пересчёте шекелей ;)',
        'count_students': 0
    }
]

for info in infos:
    requests.post('http://localhost:8000/majors/add/', json=info)
