from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker, get_current_user
from models import Disponibilita, Utente
from schemas.disponibilita import DisponibilitaCreate, DisponibilitaRead, DisponibilitaUpdate
from services.disponibilita import DisponibilitaService, slot_e_libero

router = APIRouter(prefix="/api/disponibilita", tags=["disponibilita"])


def a_disponibilita_read(disponibilita: Disponibilita) -> DisponibilitaRead:
    return DisponibilitaRead(
        id=disponibilita.id,
        medico_id=disponibilita.medico_id,
        sede_id=disponibilita.sede_id,
        data=disponibilita.data,
        ora_inizio=disponibilita.ora_inizio,
        ora_fine=disponibilita.ora_fine,
        libera=slot_e_libero(disponibilita),
    )


def _medico_id_del_richiedente(utente: Utente) -> int:
    if utente.medico is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un medico può gestire le proprie disponibilità",
        )
    return utente.medico.id


@router.get(
    "",
    response_model=list[DisponibilitaRead],
    summary="Elenco degli slot liberi, filtrabile per medico e sede",
)
def get_disponibilita_libere(
    medico_id: int | None = None, sede_id: int | None = None, db: Session = Depends(get_db)
):
    libere = DisponibilitaService(db).list_libere(medico_id, sede_id)
    return [a_disponibilita_read(d) for d in libere]


@router.post(
    "",
    response_model=DisponibilitaRead,
    status_code=status.HTTP_201_CREATED,
    summary="Il medico autenticato crea una propria fascia di disponibilità",
    dependencies=[Depends(RoleChecker(["medico"]))],
)
def create_disponibilita(
    payload: DisponibilitaCreate,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    medico_id = _medico_id_del_richiedente(utente)
    try:
        disponibilita = DisponibilitaService(db).create(
            medico_id=medico_id,
            sede_id=payload.sede_id,
            data=payload.data,
            ora_inizio=payload.ora_inizio,
            ora_fine=payload.ora_fine,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return a_disponibilita_read(disponibilita)


@router.put(
    "/{disponibilita_id}",
    response_model=DisponibilitaRead,
    summary="Modifica una fascia di disponibilità, solo se libera (medico proprietario o admin)",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def update_disponibilita(
    disponibilita_id: int,
    payload: DisponibilitaUpdate,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    richiedente_medico_id = None if utente.ruolo == "admin" else _medico_id_del_richiedente(utente)
    try:
        disponibilita = DisponibilitaService(db).update(
            disponibilita_id,
            richiedente_medico_id,
            sede_id=payload.sede_id,
            data=payload.data,
            ora_inizio=payload.ora_inizio,
            ora_fine=payload.ora_fine,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return a_disponibilita_read(disponibilita)


@router.delete(
    "/{disponibilita_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina una fascia di disponibilità, solo se libera (medico proprietario o admin)",
    dependencies=[Depends(RoleChecker(["medico", "admin"]))],
)
def delete_disponibilita(
    disponibilita_id: int,
    utente: Utente = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    richiedente_medico_id = None if utente.ruolo == "admin" else _medico_id_del_richiedente(utente)
    try:
        DisponibilitaService(db).delete(disponibilita_id, richiedente_medico_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
