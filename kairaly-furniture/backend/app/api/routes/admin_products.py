import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.config import settings
from app.crud.branch import get_branch
from app.crud.product import (
    add_product_images,
    create_product,
    delete_product,
    delete_product_image,
    get_product,
    list_products,
    update_product,
    update_stock,
)
from app.database import get_db
from app.models.user import User
from app.schemas.product import (
    PaginatedProducts,
    ProductCreate,
    ProductListItem,
    ProductRead,
    ProductUpdate,
    SortOption,
    StockUpdate,
)
router = APIRouter(prefix="/admin/products", tags=["Admin - Products"])

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def _validate_branch_exists(db: Session, branch_id: int) -> None:
    if get_branch(db, branch_id) is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"branch_id {branch_id} does not exist")


def _get_product_or_404(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.get(
    "",
    response_model=PaginatedProducts,
    summary="List ALL products across both branches (admin management view)",
)
def admin_list_products(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
    branch_id: int | None = Query(None),
    search: str | None = Query(None),
    sort: SortOption = Query(SortOption.NEWEST),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    items, total = list_products(
        db, branch_id=branch_id, search=search, sort=sort, page=page, page_size=page_size
    )
    return PaginatedProducts(
        total=total, page=page, page_size=page_size, items=[ProductListItem.model_validate(p) for p in items]
    )


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Add a new sofa")
def admin_create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    _validate_branch_exists(db, product_in.branch_id)
    product = create_product(db, product_in)
    return get_product(db, product.id)


@router.put("/{product_id}", response_model=ProductRead, summary="Edit a sofa's details")
def admin_update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    product = _get_product_or_404(db, product_id)
    if product_in.branch_id is not None:
        _validate_branch_exists(db, product_in.branch_id)
    updated = update_product(db, product, product_in)
    return get_product(db, updated.id)


@router.patch("/{product_id}/stock", response_model=ProductRead, summary="Update stock count only")
def admin_update_stock(
    product_id: int,
    stock_in: StockUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    product = _get_product_or_404(db, product_id)
    update_stock(db, product, stock_in.stock_count)
    return get_product(db, product_id)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a sofa")
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    product = _get_product_or_404(db, product_id)
    delete_product(db, product)


@router.post(
    "/{product_id}/images",
    response_model=ProductRead,
    summary="Upload one or more images for a sofa",
)
def admin_upload_images(
    product_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    product = _get_product_or_404(db, product_id)

    max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    saved_urls: list[str] = []
    for file in files:
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image type '{ext}'. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}",
            )

        contents = file.file.read()
        if len(contents) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image '{file.filename}' exceeds max size of {settings.MAX_IMAGE_SIZE_MB}MB",
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, "wb") as f:
            f.write(contents)

        saved_urls.append(f"/static/uploads/{filename}")

    add_product_images(db, product, saved_urls)
    return get_product(db, product_id)


@router.delete(
    "/{product_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific product image",
)
def admin_delete_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    product = _get_product_or_404(db, product_id)
    if not delete_product_image(db, product, image_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found on this product")
