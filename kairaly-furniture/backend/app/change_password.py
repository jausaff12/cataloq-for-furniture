"""
One-time utility to change the admin password directly in the database.
Run with:  python -m app.change_password
"""
import getpass

from app.core.security import hash_password
from app.crud.user import get_user_by_username
from app.database import SessionLocal


def run():
    username = input("Admin username to update (e.g. admin): ").strip()
    new_password = getpass.getpass("New password: ").strip()
    confirm = getpass.getpass("Confirm new password: ").strip()

    if new_password != confirm:
        print("Passwords don't match. Nothing changed.")
        return
    if len(new_password) < 8:
        print("Password must be at least 8 characters. Nothing changed.")
        return

    db = SessionLocal()
    try:
        user = get_user_by_username(db, username)
        if user is None:
            print(f"No user found with username '{username}'.")
            return
        user.hashed_password = hash_password(new_password)
        db.add(user)
        db.commit()
        print(f"Password updated successfully for '{username}'.")
    finally:
        db.close()


if __name__ == "__main__":
    run()