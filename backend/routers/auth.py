from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker, get_current_user
from models import Utente
from repositories.utente import UtenteRepository
from schemas.auth import LoginRequest, RegisterPazienteRequest, TokenRead
from schemas.utente import UtenteDettaglio, UtenteEdit, UtenteEditRequest, UtenteRead
from services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _a_utente_dettaglio(utente: Utente) -> UtenteDettaglio:
    nome = cognome = telefono = codice_fiscale = numero_albo = None
    if utente.paziente:
        nome = utente.paziente.nome
        cognome = utente.paziente.cognome
        telefono = utente.paziente.telefono
        codice_fiscale = utente.paziente.codice_fiscale
    elif utente.medico:
        nome = utente.medico.nome
        cognome = utente.medico.cognome
        numero_albo = utente.medico.numero_albo

    return UtenteDettaglio(
        id=utente.id,
        email=utente.email,
        ruolo=utente.ruolo,
        is_active=utente.is_active,
        created_at=utente.created_at,
        nome=nome,
        cognome=cognome,
        telefono=telefono,
        codice_fiscale=codice_fiscale,
        numero_albo=numero_albo,
    )


@router.post(
    "/register",
    response_model=UtenteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registra un nuovo paziente",
)
def register(payload: RegisterPazienteRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.register_paziente(
            email=payload.email,
            password=payload.password,
            nome=payload.nome,
            cognome=payload.cognome,
            codice_fiscale=payload.codice_fiscale,
            data_nascita=payload.data_nascita,
            telefono=payload.telefono,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenRead, summary="Login e ottenimento del token JWT")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.login(email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UtenteRead, summary="Dati dell'utente autenticato")
def me(utente: Utente = Depends(get_current_user)):
    return utente


@router.get(
    "/users/{user_id}",
    response_model=UtenteDettaglio,
    dependencies=[Depends(RoleChecker(["admin"]))],
    summary="Dettaglio di un utente per id (solo admin)",
)
def get_utente(user_id: int, db: Session = Depends(get_db)):
    utente = UtenteRepository(db).get_by_id(user_id)
    if utente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utente non trovato")
    return _a_utente_dettaglio(utente)


@router.get(
    "/users",
    response_model=list[UtenteDettaglio],
    dependencies=[Depends(RoleChecker(["admin"]))],
    summary="Elenco di tutti gli utenti (solo admin)",
)
def get_utenti(db: Session = Depends(get_db)):
    return [_a_utente_dettaglio(u) for u in UtenteRepository(db).get_all()]


@router.put(
    "/users/{user_id}",
    response_model=UtenteEdit,
    dependencies=[Depends(RoleChecker(["admin"]))],
    summary="Modifica il profilo di un paziente (solo admin)",
)
def update_utente(user_id: int, payload: UtenteEditRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        utente = service.update_utente(
            user_id,
            nome=payload.nome,
            cognome=payload.cognome,
            telefono=payload.telefono,
        )
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UtenteEdit(
        id=utente.id,
        email=utente.email,
        nome=utente.paziente.nome,
        cognome=utente.paziente.cognome,
        codice_fiscale=utente.paziente.codice_fiscale,
        data_nascita=utente.paziente.data_nascita,
        telefono=utente.paziente.telefono,
    )