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

        if self.db.query(Paziente).filter_by(codice_fiscale=codice_fiscale).first():
            raise ValueError("Codice fiscale già registrato")

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
        numero_albo: str | None = None,
        is_active: bool | None = None,
    ) -> Utente:
        utente = self.utente_repository.get_by_id(user_id)
        if utente is None:
            raise LookupError("Utente non trovato")

        if is_active is not None:
            utente.is_active = is_active

        profilo = utente.paziente or utente.medico
        if nome is not None or cognome is not None:
            if profilo is None:
                raise ValueError("Questo utente non ha un profilo modificabile")
            if nome is not None:
                profilo.nome = nome
            if cognome is not None:
                profilo.cognome = cognome
        if telefono is not None:
            if utente.paziente is None:
                raise ValueError("Il telefono è modificabile solo per i pazienti")
            utente.paziente.telefono = telefono
        if numero_albo is not None:
            if utente.medico is None:
                raise ValueError("Il numero albo è modificabile solo per i medici")
            utente.medico.numero_albo = numero_albo

        self.db.commit()
        self.db.refresh(utente)
        return utente

    def login(self, email: str, password: str) -> TokenRead:
        utente = self.utente_repository.find_by_email(email)
        if utente is None or not verify_password(password, utente.password_hash):
            raise ValueError("Credenziali non valide")
        if not utente.is_active:
            raise ValueError("Utente disabilitato, contattare un amministratore per maggiori dettagli")

        token = self.jwt_handler.create_token({"sub": str(utente.id), "ruolo": utente.ruolo})
        return TokenRead(access_token=token)
