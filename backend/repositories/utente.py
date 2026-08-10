from sqlalchemy import select
from sqlalchemy.orm import Session

from models.utente import Utente
from repositories.base import BaseRepository


class UtenteRepository(BaseRepository[Utente]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Utente)

    def find_by_email(self, email: str) -> Utente | None:
        return self.db.scalar(select(Utente).where(Utente.email == email))