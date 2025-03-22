from typing import Any, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class UserContext:

  business_domain: str = None
  db: AsyncSession

  def __init__(self) -> None:
    pass

class Response(BaseModel):
    data: Optional[Any] = None
    message: Optional[str] = "Success"
    error: bool = False
    status_code: Optional[int] = 200