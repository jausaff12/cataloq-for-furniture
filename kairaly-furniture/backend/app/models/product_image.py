from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class ProductImage(Base):
    """One of possibly many images belonging to a product."""

    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)

    product = relationship("Product", back_populates="images")

    def __repr__(self) -> str:
        return f"<ProductImage id={self.id} product_id={self.product_id}>"
