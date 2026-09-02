from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker, get_current_user
from models import Utente
from repositories.appuntamento import AppuntamentoRepository
from schemas.appuntamento import AppuntamentoCreate, AppuntamentoRead
from schemas.referto import RefertoRead
from services.appuntamento import AppuntamentoService, SlotNonDisponibileError
from services.referto import RefertoService

router = APIRouter(prefix="/api/appuntamenti", tags=["appuntamenti"])


def _e_parte_in_causa(utente: Utente, appuntamento) -> bool:
    if utente.ruolo == "admin":
        return True
    if utente.paziente is not None and appuntamento.paziente_id == utente.paziente.id:
        return True
    if utente.medico is not None and appuntamento.medico_id == utente.medico.id:
        return True
    return False


def _medico_id_del_richiedente(utente: Utente) -> int:
    if utente.medico is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un medico può caricare un referto",
        )
    return utente.medico.id


def _get_o_404(db: Session, appuntamento_id: int):
    appuntamento = AppuntamentoRepository(db).get_by_id(appuntamento_id)
    if appuntamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appuntamento non trovato"
        )
    return appuntamento


def _verifica_accesso(utente: Utente, appuntamento) -> None:
    if not _e_parte_in_causa(utente, appuntamento):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Non hai accesso a questo appuntamento"
        )


@router.post(
    "",
    response_model=AppuntamentoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Il paziente autenticato prenota un appuntamento",
    dependencies=[Depends(RoleChecker(["paziente"]))],
)
def prenota_appuntamento(
    payload: AppuntamentoCreate,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return AppuntamentoService(db).prenota(
            paziente_id=utente.paziente.id,
            disponibilita_id=payload.disponibilita_id,
            prestazione_id=payload.prestazione_id,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SlotNonDisponibileError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "",
    response_model=list[AppuntamentoRead],
    summary="Elenco appuntamenti, filtrato in base al ruolo dell'utente autenticato",
)
def get_appuntamenti(utente: Utente = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = AppuntamentoRepository(db)
    if utente.ruolo == "admin":
        return repository.get_all()
    if utente.ruolo == "medico" and utente.medico is not None:
        return repository.find_by_medico(utente.medico.id)
    if utente.ruolo == "paziente" and utente.paziente is not None:
        return repository.find_by_paziente(utente.paziente.id)
    return []


@router.get(
    "/{appuntamento_id}",
    response_model=AppuntamentoRead,
    summary="Dettaglio di un appuntamento (solo chi ne è parte, o admin)",
)
def get_appuntamento(
    appuntamento_id: int,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appuntamento = _get_o_404(db, appuntamento_id)
    _verifica_accesso(utente, appuntamento)
    return appuntamento


@router.patch(
    "/{appuntamento_id}/annulla",
    response_model=AppuntamentoRead,
    summary="Annulla un appuntamento e libera lo slot (paziente, medico coinvolti, o admin)",
)
def annulla_appuntamento(
    appuntamento_id: int,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appuntamento = _get_o_404(db, appuntamento_id)
    _verifica_accesso(utente, appuntamento)
    try:
        return AppuntamentoService(db).annulla(appuntamento)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{appuntamento_id}/conferma",
    response_model=AppuntamentoRead,
    summary="Il medico (o admin) conferma un appuntamento prenotato",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def conferma_appuntamento(
    appuntamento_id: int,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appuntamento = _get_o_404(db, appuntamento_id)
    _verifica_accesso(utente, appuntamento)
    try:
        return AppuntamentoService(db).conferma(appuntamento)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    "/{appuntamento_id}/completa",
    response_model=AppuntamentoRead,
    summary="Il medico (o admin) segna un appuntamento come completato",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def completa_appuntamento(
    appuntamento_id: int,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appuntamento = _get_o_404(db, appuntamento_id)
    _verifica_accesso(utente, appuntamento)
    try:
        return AppuntamentoService(db).completa(appuntamento)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/{appuntamento_id}/referto",
    response_model=RefertoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Il medico (o admin) carica il referto di un appuntamento completato",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
async def carica_referto(
    appuntamento_id: int,
    file: UploadFile = File(...),
    descrizione: str | None = Form(None),
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    richiedente_medico_id = None if utente.ruolo == "admin" else _medico_id_del_richiedente(utente)
    contenuto = await file.read()
    try:
        return RefertoService(db).carica(
            appuntamento_id=appuntamento_id,
            richiedente_medico_id=richiedente_medico_id,
            content_type=file.content_type,
            contenuto=contenuto,
            descrizione=descrizione,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
