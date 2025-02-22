from fastapi import FastAPI
from app.students.router import router as router_students
from app.major.router import router as router_majors
from app.courses.router import router as router_courses
from app.users.router import router as router_users

app = FastAPI()

@app.get("/")
async def home_page():
    return {"message": "Hello World"}


app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_courses)
app.include_router(router_users)
