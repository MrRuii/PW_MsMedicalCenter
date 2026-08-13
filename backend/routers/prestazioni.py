from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker
from schemas.prestazione import PrestazioneCreate, PrestazioneRead, PrestazioneUpdate
from services.prestazione import PrestazioneService

router = APIRouter(prefix="/api/prestazioni", tags=["prestazioni"])


@router.get(
    "",
    response_model=list[PrestazioneRead],
    summary="Elenco delle prestazioni, filtrabile per specialità",
)
def get_prestazioni(specialita_id: int | None = None, db: Session = Depends(get_db)):
    return PrestazioneService(db).list(specialita_id)


@router.post(
    "",
    response_model=PrestazioneRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crea una prestazione (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def create_prestazione(payload: PrestazioneCreate, db: Session = Depends(get_db)):
    try:
        return PrestazioneService(db).create(
            specialita_id=payload.specialita_id,
            nome=payload.nome,
            durata_min=payload.durata_min,
            prezzo=payload.prezzo,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{prestazione_id}",
    response_model=PrestazioneRead,
    summary="Modifica una prestazione (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def update_prestazione(
    prestazione_id: int, payload: PrestazioneUpdate, db: Session = Depends(get_db)
):
    try:
        return PrestazioneService(db).update(
            prestazione_id,
            specialita_id=payload.specialita_id,
            nome=payload.nome,
            durata_min=payload.durata_min,
            prezzo=payload.prezzo,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{prestazione_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una prestazione (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def delete_prestazione(prestazione_id: int, db: Session = Depends(get_db)):
    try:
        PrestazioneService(db).delete(prestazione_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
