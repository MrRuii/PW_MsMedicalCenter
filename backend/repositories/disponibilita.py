from sqlalchemy import select
from sqlalchemy.orm import Session

from models.appuntamento import Appuntamento
from models.disponibilita import Disponibilita
from repositories.base import BaseRepository


class DisponibilitaRepository(BaseRepository[Disponibilita]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Disponibilita)

    def find_by_medico(self, medico_id: int) -> list[Disponibilita]:
        return list(
            self.db.scalars(
                select(Disponibilita).where(Disponibilita.medico_id == medico_id)
            )
        )

    def find_libere(
        self, medico_id: int | None = None, sede_id: int | None = None
    ) -> list[Disponibilita]:
        # Uno slot e' libero se non ha un appuntamento, o se quell'appuntamento e' annullato
        query = select(Disponibilita).where(
            ~Disponibilita.appuntamento.has(Appuntamento.stato != "annullato")
        )
        if medico_id is not None:
            query = query.where(Disponibilita.medico_id == medico_id)
        if sede_id is not None:
            query = query.where(Disponibilita.sede_id == sede_id)
        return list(self.db.scalars(query))
