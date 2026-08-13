from sqlalchemy.orm import Session

from models import Prestazione
from repositories.prestazione import PrestazioneRepository
from repositories.specialita import SpecialitaRepository


class PrestazioneService:
    def __init__(self, db: Session) -> None:
        self.prestazione_repository = PrestazioneRepository(db)
        self.specialita_repository = SpecialitaRepository(db)

    def list(self, specialita_id: int | None = None) -> list[Prestazione]:
        if specialita_id is not None:
            return self.prestazione_repository.find_by_specialita(specialita_id)
        return self.prestazione_repository.get_all()

    def create(
        self, specialita_id: int, nome: str, durata_min: int, prezzo: float
    ) -> Prestazione:
        if self.specialita_repository.get_by_id(specialita_id) is None:
            raise LookupError("Specialita non trovata")

        prestazione = Prestazione(
            specialita_id=specialita_id, nome=nome, durata_min=durata_min, prezzo=prezzo
        )
        return self.prestazione_repository.create(prestazione)

    def update(
        self,
        prestazione_id: int,
        specialita_id: int | None = None,
        nome: str | None = None,
        durata_min: int | None = None,
        prezzo: float | None = None,
    ) -> Prestazione:
        prestazione = self.prestazione_repository.get_by_id(prestazione_id)
        if prestazione is None:
            raise LookupError("Prestazione non trovata")

        if specialita_id is not None:
            if self.specialita_repository.get_by_id(specialita_id) is None:
                raise LookupError("Specialita non trovata")
            prestazione.specialita_id = specialita_id
        if nome is not None:
            prestazione.nome = nome
        if durata_min is not None:
            prestazione.durata_min = durata_min
        if prezzo is not None:
            prestazione.prezzo = prezzo

        return self.prestazione_repository.update(prestazione)

    def delete(self, prestazione_id: int) -> None:
        if not self.prestazione_repository.delete(prestazione_id):
            raise LookupError("Prestazione non trovata")
