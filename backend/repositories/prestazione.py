from sqlalchemy import select
from sqlalchemy.orm import Session

from models.prestazione import Prestazione
from repositories.base import BaseRepository


class PrestazioneRepository(BaseRepository[Prestazione]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Prestazione)

    def find_by_specialita(self, specialita_id: int) -> list[Prestazione]:
        return list(
            self.db.scalars(
                select(Prestazione).where(Prestazione.specialita_id == specialita_id)
            )
        )
