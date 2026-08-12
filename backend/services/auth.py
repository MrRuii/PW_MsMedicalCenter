from datetime import date

from sqlalchemy.orm import Session

from core.security import JWTHandler, hash_password, verify_password
from models import Paziente, Utente
from repositories.utente import UtenteRepository
from schemas.auth import TokenRead


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.utente_repository = UtenteRepository(db)
        self.jwt_handler = JWTHandler()

    def register_paziente(
        self,
        email: str,
        password: str,
        nome: str,
        cognome: str,
        codice_fiscale: str,
        data_nascita: date | None = None,
        telefono: str | None = None,
    ) -> Utente:
        if self.utente_repository.find_by_email(email):
            raise ValueError("Email già registrata")

        utente = Utente(
            email=email,
            password_hash=hash_password(password),
            ruolo="paziente",
            is_active=True,
        )
        self.db.add(utente)
        self.db.flush()

        paziente = Paziente(
            utente_id=utente.id,
            nome=nome,
            cognome=cognome,
            codice_fiscale=codice_fiscale,
            data_nascita=data_nascita,
            telefono=telefono,
        )
        self.db.add(paziente)
        self.db.commit()
        self.db.refresh(utente)
        return utente

    def update_utente(
        self,
        user_id: int,
        nome: str | None = None,
        cognome: str | None = None,
        telefono: str | None = None,
    ) -> Utente:
        utente = self.utente_repository.get_by_id(user_id)
        if utente is None:
            raise LookupError("Utente non trovato")
        if utente.paziente is None:
            raise ValueError("Questo utente non ha un profilo paziente modificabile")

        if nome is not None:
            utente.paziente.nome = nome
        if cognome is not None:
            utente.paziente.cognome = cognome
        if telefono is not None:
            utente.paziente.telefono = telefono

        self.db.commit()
        self.db.refresh(utente)
        return utente

    def login(self, email: str, password: str) -> TokenRead:
        utente = self.utente_repository.find_by_email(email)
        if utente is None or not verify_password(password, utente.password_hash):
            raise ValueError("Credenziali non valide")

        token = self.jwt_handler.create_token({"sub": str(utente.id), "ruolo": utente.ruolo})
        return TokenRead(access_token=token)
