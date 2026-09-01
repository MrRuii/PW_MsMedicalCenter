from sqlalchemy import select
from sqlalchemy.orm import Session

from models.medico import Medico
from repositories.base import BaseRepository


class MedicoRepository(BaseRepository[Medico]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Medico)

    def find_by_specialita(self, specialita_id: int) -> list[Medico]:
        return list(
            self.db.scalars(
                select(Medico).where(Medico.specialita.any(id=specialita_id))
            )
        )
