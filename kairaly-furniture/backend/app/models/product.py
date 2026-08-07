from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Product(Base):
    """
    A sofa product. The MVP only deals with the 'sofa' category, but a category
    column is kept so future product types can be added without a schema rewrite.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # --- Core info ---
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(50), nullable=False, default="sofa", index=True)
    # Numeric price is no longer shown to customers; kept nullable for potential
    # future internal/back-office use. Public-facing pricing is the tier below.
    price = Column(Float, nullable=True)
    price_tier = Column(String(20), nullable=False, default="Moderate", index=True)
    description = Column(Text, nullable=True)
    stock_count = Column(Integer, nullable=False, default=0)

    # --- Branch ---
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)
    branch = relationship("Branch", back_populates="products")

    # --- Dimensions ---
    length_in = Column(Float, nullable=True)
    width_in = Column(Float, nullable=True)
    height_in = Column(Float, nullable=True)

    # --- Sofa-specific attributes ---
    seating_capacity = Column(Integer, nullable=True)
    foam_thickness_in = Column(Float, nullable=True)
    foam_type = Column(String(100), nullable=True, index=True)
    fabric_material = Column(String(100), nullable=True, index=True)
    frame_material = Column(String(100), nullable=True)
    color = Column(String(100), nullable=True)
    warranty = Column(String(100), nullable=True)

    # Stored as a comma-separated string, e.g. "Grey,Beige,Navy Blue"
    available_colors = Column(String(500), nullable=True)

    # --- Timestamps ---
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.display_order",
    )

    __table_args__ = (
        CheckConstraint("price >= 0 OR price IS NULL", name="ck_products_price_non_negative"),
        CheckConstraint("stock_count >= 0", name="ck_products_stock_non_negative"),
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} branch_id={self.branch_id}>"
