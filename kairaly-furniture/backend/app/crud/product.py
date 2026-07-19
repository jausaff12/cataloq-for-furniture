from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload

from app.models.product import Product
from app.models.product_image import ProductImage
from app.schemas.product import ProductCreate, ProductUpdate, SortOption


def _attach_primary_image(product: Product) -> Product:
    """Attach a dynamic `primary_image` attribute (not a DB column) for list responses."""
    primary = next((img for img in product.images if img.is_primary), None)
    if primary is None and product.images:
        primary = product.images[0]
    product.primary_image = primary.image_url if primary else None
    return product


def _serialize_colors(colors: list[str] | None) -> str | None:
    if not colors:
        return None
    return ",".join(colors)


def get_product(db: Session, product_id: int) -> Product | None:
    return (
        db.query(Product)
        .options(joinedload(Product.images), joinedload(Product.branch))
        .filter(Product.id == product_id)
        .first()
    )


def list_products(
    db: Session,
    *,
    visiting_branch_id: int | None = None,
    exclude_branch_id: int | None = None,
    branch_id: int | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    fabric_material: str | None = None,
    foam_type: str | None = None,
    sort: SortOption = SortOption.NEWEST,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    """
    Core catalog query.

    Business rule: a customer physically standing in one branch should only see
    sofas stocked at the OTHER branch. Callers implement this by resolving the
    "visiting" branch to its opposite branch_id before calling this function
    (see api/routes/products.py), or by passing `exclude_branch_id` directly.
    """
    query = db.query(Product).options(joinedload(Product.images), joinedload(Product.branch))

    if branch_id is not None:
        query = query.filter(Product.branch_id == branch_id)
    if exclude_branch_id is not None:
        query = query.filter(Product.branch_id != exclude_branch_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search.strip()}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if fabric_material:
        query = query.filter(Product.fabric_material.ilike(f"%{fabric_material.strip()}%"))
    if foam_type:
        query = query.filter(Product.foam_type.ilike(f"%{foam_type.strip()}%"))

    sort_map = {
        SortOption.NEWEST: desc(Product.created_at),
        SortOption.OLDEST: asc(Product.created_at),
        SortOption.PRICE_LOW_TO_HIGH: asc(Product.price),
        SortOption.PRICE_HIGH_TO_LOW: desc(Product.price),
    }
    query = query.order_by(sort_map.get(sort, desc(Product.created_at)), desc(Product.id))

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    items = [_attach_primary_image(p) for p in items]
    return items, total


def create_product(db: Session, product_in: ProductCreate) -> Product:
    data = product_in.model_dump(exclude={"available_colors"})
    product = Product(**data, available_colors=_serialize_colors(product_in.available_colors))
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, product_in: ProductUpdate) -> Product:
    update_data = product_in.model_dump(exclude_unset=True, exclude={"available_colors"})
    for field, value in update_data.items():
        setattr(product, field, value)

    if "available_colors" in product_in.model_fields_set:
        product.available_colors = _serialize_colors(product_in.available_colors)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_stock(db: Session, product: Product, stock_count: int) -> Product:
    product.stock_count = stock_count
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def add_product_images(db: Session, product: Product, image_urls: list[str]) -> Product:
    existing_count = len(product.images)
    for i, url in enumerate(image_urls):
        img = ProductImage(
            product_id=product.id,
            image_url=url,
            is_primary=(existing_count == 0 and i == 0),
            display_order=existing_count + i,
        )
        db.add(img)
    db.commit()
    db.refresh(product)
    return product


def delete_product_image(db: Session, product: Product, image_id: int) -> bool:
    image = next((img for img in product.images if img.id == image_id), None)
    if image is None:
        return False
    was_primary = image.is_primary
    db.delete(image)
    db.commit()
    db.refresh(product)
    # Promote another image to primary if we just removed the primary one.
    if was_primary and product.images:
        product.images[0].is_primary = True
        db.add(product.images[0])
        db.commit()
    return True
