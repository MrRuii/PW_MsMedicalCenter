from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker, get_current_user
from models import Utente
from repositories.referto import RefertoRepository
from schemas.referto import RefertoRead, RefertoUpdate
from services.referto import RefertoService

router = APIRouter(prefix="/api/referti", tags=["referti"])


def _medico_id_del_richiedente(utente: Utente) -> int:
    if utente.medico is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un medico può gestire i referti",
        )
    return utente.medico.id


def _get_o_404(db: Session, referto_id: int):
    referto = RefertoRepository(db).get_by_id(referto_id)
    if referto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referto non trovato")
    return referto


@router.get("", response_model=list[RefertoRead], summary="Elenco referti, filtrato in base al ruolo dell'utente autenticato")
def get_referti(utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)):
    return RefertoService(db).list_per_utente(utente)


@router.get(
    "/{referto_id}",
    response_model=RefertoRead,
    summary="Metadati di un referto (solo chi ne ha accesso)",
)
def get_referto(
    referto_id: int, utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)
):
    referto = _get_o_404(db, referto_id)
    if not RefertoService(db).verifica_accesso(utente, referto):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Non hai accesso a questo referto"
        )
    return referto


@router.get(
    "/{referto_id}/file",
    summary="Scarica il file del referto (solo chi ne ha accesso)",
)
def scarica_referto(
    referto_id: int, utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)
):
    referto = _get_o_404(db, referto_id)
    if not RefertoService(db).verifica_accesso(utente, referto):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Non hai accesso a questo referto"
        )
    estensione = Path(referto.file_path).suffix
    nome_scaricato = f"referto-{referto.appuntamento_id}{estensione}"
    return FileResponse(referto.file_path, filename=nome_scaricato)


@router.put(
    "/{referto_id}",
    response_model=RefertoRead,
    summary="Aggiorna la descrizione di un referto (medico proprietario o admin)",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def aggiorna_referto(
    referto_id: int,
    payload: RefertoUpdate,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    richiedente_medico_id = None if utente.ruolo == "admin" else _medico_id_del_richiedente(utente)
    try:
        return RefertoService(db).aggiorna_descrizione(
            referto_id, richiedente_medico_id, payload.descrizione
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete(
    "/{referto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina un referto (medico proprietario o admin)",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def elimina_referto(
    referto_id: int, utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)
):
    richiedente_medico_id = None if utente.ruolo == "admin" else _medico_id_del_richiedente(utente)
    try:
        RefertoService(db).elimina(referto_id, richiedente_medico_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
