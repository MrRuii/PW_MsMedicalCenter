from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker
from repositories.disponibilita import DisponibilitaRepository
from repositories.medico import MedicoRepository
from routers.disponibilita import a_disponibilita_read
from schemas.disponibilita import DisponibilitaRead
from schemas.medico import MedicoCreate, MedicoRead, MedicoUpdate
from services.medico import MedicoService

router = APIRouter(prefix="/api/medici", tags=["medici"])


@router.get(
    "", response_model=list[MedicoRead], summary="Elenco dei medici, filtrabile per specialità"
)
def get_medici(specialita_id: int | None = None, db: Session = Depends(get_db)):
    return MedicoService(db).list(specialita_id)


@router.get("/{medico_id}", response_model=MedicoRead, summary="Dettaglio di un medico")
def get_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = MedicoRepository(db).get_by_id(medico_id)
    if medico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medico non trovato")
    return medico


@router.get(
    "/{medico_id}/disponibilita",
    response_model=list[DisponibilitaRead],
    summary="Disponibilità (libere e occupate) di un medico",
)
def get_disponibilita_medico(medico_id: int, db: Session = Depends(get_db)):
    disponibilita = DisponibilitaRepository(db).find_by_medico(medico_id)
    return [a_disponibilita_read(d) for d in disponibilita]


@router.post(
    "",
    response_model=MedicoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crea un medico (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def create_medico(payload: MedicoCreate, db: Session = Depends(get_db)):
    try:
        return MedicoService(db).create(
            email=payload.email,
            password=payload.password,
            nome=payload.nome,
            cognome=payload.cognome,
            numero_albo=payload.numero_albo,
            specialita_ids=payload.specialita_ids,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/{medico_id}",
    response_model=MedicoRead,
    summary="Modifica un medico (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def update_medico(medico_id: int, payload: MedicoUpdate, db: Session = Depends(get_db)):
    try:
        return MedicoService(db).update(
            medico_id,
            nome=payload.nome,
            cognome=payload.cognome,
            numero_albo=payload.numero_albo,
            specialita_ids=payload.specialita_ids,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{medico_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Elimina un medico (solo admin)",
    dependencies=[Depends(RoleChecker(["admin"]))],
)
def delete_medico(medico_id: int, db: Session = Depends(get_db)):
    try:
        MedicoService(db).delete(medico_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
