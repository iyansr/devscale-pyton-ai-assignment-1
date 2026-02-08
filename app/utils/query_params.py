from fastapi import Query


def list_query_params(page: int = Query(default=1), per_page: int = Query(default=10)):
    limit = per_page
    offset = (page - 1) * per_page if per_page > 0 else 0

    return {"limit": limit, "offset": offset}
