import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"  # reserved for future use; customers never actually log in


class User(Base):
    """
    Application user. In this MVP, only ADMIN users are ever persisted/authenticated;
    customers browse anonymously and never create an account.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ADMIN)
    is_active = Column(Integer, default=1, nullable=False)  # 1 = active, 0 = disabled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role}>"
