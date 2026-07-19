import enum
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field

from app.schemas.branch import BranchRead
from app.schemas.product_image import ProductImageRead


class SortOption(str, enum.Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    PRICE_LOW_TO_HIGH = "price_low_to_high"
    PRICE_HIGH_TO_LOW = "price_high_to_low"


class StockStatus(str, enum.Enum):
    IN_STOCK = "In Stock"
    MADE_TO_ORDER = "Made to Order"


# ---------------------------------------------------------------------------
# Shared field definitions
# ---------------------------------------------------------------------------
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    description: str | None = Field(None, max_length=5000)
    branch_id: int = Field(..., gt=0)
    stock_count: int = Field(0, ge=0)

    length_cm: float | None = Field(None, gt=0)
    width_cm: float | None = Field(None, gt=0)
    height_cm: float | None = Field(None, gt=0)

    seating_capacity: int | None = Field(None, gt=0, le=20)
    foam_thickness_cm: float | None = Field(None, gt=0)
    foam_type: str | None = Field(None, max_length=100)
    fabric_material: str | None = Field(None, max_length=100)
    frame_material: str | None = Field(None, max_length=100)
    color: str | None = Field(None, max_length=100)
    warranty: str | None = Field(None, max_length=100)
    available_colors: list[str] | None = Field(default=None, description="List of available color names")

    @field_validator("available_colors")
    @classmethod
    def validate_colors(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        cleaned = [c.strip() for c in v if c and c.strip()]
        return cleaned or None


# ---------------------------------------------------------------------------
# Create / Update
# ---------------------------------------------------------------------------
class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    """All fields optional - only supplied fields are updated (PATCH-style via PUT)."""

    name: str | None = Field(None, min_length=2, max_length=200)
    price: float | None = Field(None, gt=0)
    description: str | None = Field(None, max_length=5000)
    branch_id: int | None = Field(None, gt=0)
    stock_count: int | None = Field(None, ge=0)

    length_cm: float | None = Field(None, gt=0)
    width_cm: float | None = Field(None, gt=0)
    height_cm: float | None = Field(None, gt=0)

    seating_capacity: int | None = Field(None, gt=0, le=20)
    foam_thickness_cm: float | None = Field(None, gt=0)
    foam_type: str | None = Field(None, max_length=100)
    fabric_material: str | None = Field(None, max_length=100)
    frame_material: str | None = Field(None, max_length=100)
    color: str | None = Field(None, max_length=100)
    warranty: str | None = Field(None, max_length=100)
    available_colors: list[str] | None = None

    @field_validator("available_colors")
    @classmethod
    def validate_colors(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        cleaned = [c.strip() for c in v if c and c.strip()]
        return cleaned or None


class StockUpdate(BaseModel):
    stock_count: int = Field(..., ge=0)


# ---------------------------------------------------------------------------
# Read models
# ---------------------------------------------------------------------------
class ProductListItem(BaseModel):
    """Slim representation used for catalog / listing views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    stock_count: int
    branch: BranchRead
    created_at: datetime
    primary_image: str | None = None

    @computed_field
    @property
    def stock_status(self) -> StockStatus:
        return StockStatus.IN_STOCK if self.stock_count > 0 else StockStatus.MADE_TO_ORDER


class ProductRead(BaseModel):
    """Full representation used for the product detail page."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    description: str | None
    stock_count: int
    branch: BranchRead

    length_cm: float | None
    width_cm: float | None
    height_cm: float | None

    seating_capacity: int | None
    foam_thickness_cm: float | None
    foam_type: str | None
    fabric_material: str | None
    frame_material: str | None
    color: str | None
    warranty: str | None
    available_colors: list[str] | None = None

    images: list[ProductImageRead] = []
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def stock_status(self) -> StockStatus:
        return StockStatus.IN_STOCK if self.stock_count > 0 else StockStatus.MADE_TO_ORDER

    @field_validator("available_colors", mode="before")
    @classmethod
    def split_colors(cls, v):
        # DB stores colors as a comma separated string; expose as a list.
        if v is None:
            return None
        if isinstance(v, str):
            return [c.strip() for c in v.split(",") if c.strip()]
        return v


class PaginatedProducts(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[ProductListItem]
