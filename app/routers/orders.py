from fastapi import APIRouter
from app.database.db_crud import create_order
from app.dto.dto import Response


router = APIRouter()

router.post("/orders", response_model=Response)(create_order)
