"""
DB setup routes
"""
from fastapi import APIRouter, Depends

from app.utils.dependencies import validate_domain
from app.database.db_setup import setup

router = APIRouter(
    prefix="/setup",
    tags=["setup"],
    dependencies=[Depends(validate_domain)],
    responses={404: {"description": "Not found"}},
)
router.post("/", responses={403: {"description": "Operation forbidden"}})(setup)