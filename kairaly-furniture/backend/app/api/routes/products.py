from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.branch import get_branch, get_branch_by_name
from app.crud.product import get_product, list_products
from app.database import get_db
from app.schemas.product import PaginatedProducts, ProductListItem, ProductRead, SortOption

router = APIRouter(prefix="/products", tags=["Products (Public Catalog)"])


@router.get(
    "",
    response_model=PaginatedProducts,
    summary="Browse the sofa catalog",
    description=(
        "Core catalog endpoint used by the customer-facing site.\n\n"
        "**Branch logic:** pass `visiting_branch` (or `visiting_branch_id`) for the branch the "
        "customer is physically standing in. The response will contain sofas stocked at the "
        "*other* branch only, since the customer can already see what's in front of them."
    ),
)
def browse_products(
    db: Session = Depends(get_db),
    visiting_branch: str | None = Query(
        None, description="Name of the branch the customer is currently visiting, e.g. 'Choondi'"
    ),
    visiting_branch_id: int | None = Query(
        None, description="ID of the branch the customer is currently visiting (alternative to visiting_branch)"
    ),
    search: str | None = Query(None, description="Search by product name"),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    fabric: str | None = Query(None, description="Filter by fabric material"),
    foam_type: str | None = Query(None, description="Filter by foam type"),
    sort: SortOption = Query(SortOption.NEWEST),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    exclude_branch_id = None
    if visiting_branch_id is not None:
        branch = get_branch(db, visiting_branch_id)
        if branch is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="visiting_branch_id not found")
        exclude_branch_id = branch.id
    elif visiting_branch is not None:
        branch = get_branch_by_name(db, visiting_branch)
        if branch is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="visiting_branch not found")
        exclude_branch_id = branch.id

    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="min_price cannot exceed max_price")

    items, total = list_products(
        db,
        exclude_branch_id=exclude_branch_id,
        search=search,
        min_price=min_price,
        max_price=max_price,
        fabric_material=fabric,
        foam_type=foam_type,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return PaginatedProducts(
        total=total,
        page=page,
        page_size=page_size,
        items=[ProductListItem.model_validate(p) for p in items],
    )


@router.get("/{product_id}", response_model=ProductRead, summary="Get full sofa details")
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
