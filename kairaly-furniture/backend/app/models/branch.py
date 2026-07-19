from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Branch(Base):
    """A physical store branch (e.g. Choondi, Tripunithura)."""

    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    products = relationship("Product", back_populates="branch", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Branch id={self.id} name={self.name!r}>"
