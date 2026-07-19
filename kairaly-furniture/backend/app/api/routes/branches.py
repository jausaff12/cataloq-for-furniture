from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.branch import get_all_branches
from app.database import get_db
from app.schemas.branch import BranchRead

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("", response_model=list[BranchRead], summary="List store branches")
def list_branches(db: Session = Depends(get_db)):
    """Used to render the home page 'Which branch are you visiting?' buttons."""
    return get_all_branches(db)
