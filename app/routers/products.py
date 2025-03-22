from typing import List
from fastapi import APIRouter
from app.database.db_crud import create_product, get_products
from app.dto.dto import Response

router = APIRouter()

router.get("/products", response_model=Response)(get_products)
router.post("/products", response_model=Response)(create_product)
