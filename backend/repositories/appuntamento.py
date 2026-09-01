from sqlalchemy import select
from sqlalchemy.orm import Session

from models.appuntamento import Appuntamento
from repositories.base import BaseRepository


class AppuntamentoRepository(BaseRepository[Appuntamento]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Appuntamento)

    def find_by_paziente(self, paziente_id: int) -> list[Appuntamento]:
        return list(
            self.db.scalars(
                select(Appuntamento).where(Appuntamento.paziente_id == paziente_id)
            )
        )

    def find_by_medico(self, medico_id: int) -> list[Appuntamento]:
        return list(
            self.db.scalars(
                select(Appuntamento).where(Appuntamento.medico_id == medico_id)
            )
        )

    def exists_by_slot(self, disponibilita_id: int) -> bool:
        appuntamento = self.db.scalar(
            select(Appuntamento).where(
                Appuntamento.disponibilita_id == disponibilita_id,
                Appuntamento.stato != "annullato",
            )
        )
        return appuntamento is not None
