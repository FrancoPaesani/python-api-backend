from fastapi import FastAPI

from persistence.initial_data import populate_permissions_table
from routes.auth_router import auth_router
from routes.management_router import user_router
from routes.oncology_router import oncology_router
from routes.utils_router import utils_router

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    populate_permissions_table()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(oncology_router)
app.include_router(user_router)
