from sqlalchemy import select
from sqlalchemy.orm import Session

from models.appuntamento import Appuntamento
from models.referto import Referto
from repositories.base import BaseRepository


class RefertoRepository(BaseRepository[Referto]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Referto)

    def find_by_paziente(self, paziente_id: int) -> list[Referto]:
        return list(
            self.db.scalars(
                select(Referto).join(Appuntamento).where(Appuntamento.paziente_id == paziente_id)
            )
        )

    def find_by_medico(self, medico_id: int) -> list[Referto]:
        return list(
            self.db.scalars(
                select(Referto).join(Appuntamento).where(Appuntamento.medico_id == medico_id)
            )
        )

    def find_by_appuntamento(self, appuntamento_id: int) -> Referto | None:
        return self.db.scalar(select(Referto).where(Referto.appuntamento_id == appuntamento_id))
