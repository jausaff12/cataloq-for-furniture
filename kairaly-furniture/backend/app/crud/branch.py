from sqlalchemy.orm import Session

from app.models.branch import Branch


def get_all_branches(db: Session) -> list[Branch]:
    return db.query(Branch).order_by(Branch.name).all()


def get_branch(db: Session, branch_id: int) -> Branch | None:
    return db.query(Branch).filter(Branch.id == branch_id).first()


def get_branch_by_name(db: Session, name: str) -> Branch | None:
    return db.query(Branch).filter(Branch.name.ilike(name)).first()


def get_or_create_branch(db: Session, name: str) -> Branch:
    branch = get_branch_by_name(db, name)
    if branch:
        return branch
    branch = Branch(name=name)
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch
