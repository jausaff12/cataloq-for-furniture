from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User, UserRole


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_admin_user(db: Session, username: str, password: str, email: str | None = None) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.ADMIN,
        is_active=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
