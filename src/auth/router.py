import fastapi

from src.auth import schemas


router = fastapi.APIRouter()


@router.post("/register/student/", response_model=schemas.StudentCreate, tags=["reg_student"])
def register_student(user: schemas.StudentCreate):
    return user
