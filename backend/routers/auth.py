from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import get_current_user
from models import Utente
from schemas.auth import LoginRequest, RegisterPazienteRequest, TokenRead
from schemas.utente import UtenteRead
from services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UtenteRead, status_code=status.HTTP_201_CREATED)
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


@router.post("/login", response_model=TokenRead)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.login(email=payload.email, password=payload.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UtenteRead)
def me(utente: Utente = Depends(get_current_user)):
    return utente
