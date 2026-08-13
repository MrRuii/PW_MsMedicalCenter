from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker
from schemas.sede import SedeCreate, SedeRead, SedeUpdate
from services.sede import SedeService

router = APIRouter(prefix="/api/sedi", tags=["sedi"])


@router.get("", response_model=list[SedeRead], summary="Elenco delle sedi")
def get_sedi(db: Session = Depends(get_db)):
    return SedeService(db).list()


@router.post(
    "",
    response_model=SedeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una sede (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def create_sede(payload: SedeCreate, db: Session = Depends(get_db)):
    return SedeService(db).create(nome=payload.nome, citta=payload.citta, indirizzo=payload.indirizzo)


@router.put(
    "/{sede_id}",
    response_model=SedeRead,
    summary="Modifica una sede (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def update_sede(sede_id: int, payload: SedeUpdate, db: Session = Depends(get_db)):
    try:
        return SedeService(db).update(
            sede_id, nome=payload.nome, citta=payload.citta, indirizzo=payload.indirizzo
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{sede_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una sede (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def delete_sede(sede_id: int, db: Session = Depends(get_db)):
    try:
        SedeService(db).delete(sede_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
