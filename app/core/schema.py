from pydantic import BaseModel


class Response[DataT](BaseModel):
    data: DataT


class Pagination(BaseModel):
    current_page: int
    total_records: int
    total_pages: int | None = None


class PaginatedResponse[DataT](BaseModel):
    message: str
    data: list[DataT]
    pagination: Pagination
