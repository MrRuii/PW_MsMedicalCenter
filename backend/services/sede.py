from sqlalchemy.orm import Session

from models import Sede
from repositories.sede import SedeRepository


class SedeService:
    def __init__(self, db: Session) -> None:
        self.sede_repository = SedeRepository(db)

    def list(self) -> list[Sede]:
        return self.sede_repository.get_all()

    def create(self, nome: str, citta: str, indirizzo: str) -> Sede:
        sede = Sede(nome=nome, citta=citta, indirizzo=indirizzo)
        return self.sede_repository.create(sede)

    def update(
        self,
        sede_id: int,
        nome: str | None = None,
        citta: str | None = None,
        indirizzo: str | None = None,
    ) -> Sede:
        sede = self.sede_repository.get_by_id(sede_id)
        if sede is None:
            raise LookupError("Sede non trovata")

        if nome is not None:
            sede.nome = nome
        if citta is not None:
            sede.citta = citta
        if indirizzo is not None:
            sede.indirizzo = indirizzo

        return self.sede_repository.update(sede)

    def delete(self, sede_id: int) -> None:
        if not self.sede_repository.delete(sede_id):
            raise LookupError("Sede non trovata")
