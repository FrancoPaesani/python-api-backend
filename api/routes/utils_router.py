from fastapi import APIRouter
from fastapi.responses import JSONResponse

from config import VERSION


utils_router = APIRouter(prefix="/utils", tags=["UTILS"])


@utils_router.get("/healthcheck/")
def healthcheck():
    return JSONResponse(content={}, status_code=200)


@utils_router.get("/version/")
def version():
    return JSONResponse(content={"version": VERSION}, status_code=200)
