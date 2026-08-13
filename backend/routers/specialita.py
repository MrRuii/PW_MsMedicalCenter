from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repositories.specialita import SpecialitaRepository
from schemas.specialita import SpecialitaRead

router = APIRouter(prefix="/api/specialita", tags=["specialita"])


@router.get("", response_model=list[SpecialitaRead], summary="Elenco delle specialità")
def get_specialita(db: Session = Depends(get_db)):
    return SpecialitaRepository(db).get_all()
