from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

def paginate(items: List[T], total: int, page: int, size: int) -> PaginatedResponse[T]:
    pages = (total + size - 1) // size
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )
