import fastapi

from src.company import schemas
from src.company import crud


company_router = fastapi.APIRouter()


@company_router.post("/register/company/")
async def register_company(
    data: schemas.CompanyCreate,
):
    company = await crud.register_company(data)
    if company is None:
        raise fastapi.HTTPException(status_code=403, detail="Email exists")
    return company
