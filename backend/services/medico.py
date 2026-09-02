from sqlalchemy.orm import Session

from core.security import hash_password
from models import Medico, Specialita, Utente
from repositories.medico import MedicoRepository
from repositories.specialita import SpecialitaRepository
from repositories.utente import UtenteRepository


class MedicoService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.medico_repository = MedicoRepository(db)
        self.utente_repository = UtenteRepository(db)
        self.specialita_repository = SpecialitaRepository(db)

    def list(self, specialita_id: int | None = None) -> list[Medico]:
        if specialita_id is not None:
            return self.medico_repository.find_by_specialita(specialita_id)
        return self.medico_repository.get_all()

    def _risolvi_specialita(self, specialita_ids: list[int]) -> list[Specialita]:
        risolte = []
        for specialita_id in specialita_ids:
            specialita = self.specialita_repository.get_by_id(specialita_id)
            if specialita is None:
                raise LookupError(f"Specialita {specialita_id} non trovata")
            risolte.append(specialita)
        return risolte

    def create(
        self,
        email: str,
        password: str,
        nome: str,
        cognome: str,
        numero_albo: str | None,
        specialita_ids: list[int],
    ) -> Medico:
        if self.utente_repository.find_by_email(email):
            raise ValueError("Email già registrata")

        specialita = self._risolvi_specialita(specialita_ids)

        utente = Utente(
            email=email,
            password_hash=hash_password(password),
            ruolo="medico",
            is_active=True,
        )
        self.db.add(utente)
        self.db.flush()

        medico = Medico(
            utente_id=utente.id,
            nome=nome,
            cognome=cognome,
            numero_albo=numero_albo,
            specialita=specialita,
        )
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def update(
        self,
        medico_id: int,
        nome: str | None = None,
        cognome: str | None = None,
        numero_albo: str | None = None,
        specialita_ids: list[int] | None = None,
    ) -> Medico:
        medico = self.medico_repository.get_by_id(medico_id)
        if medico is None:
            raise LookupError("Medico non trovato")

        if nome is not None:
            medico.nome = nome
        if cognome is not None:
            medico.cognome = cognome
        if numero_albo is not None:
            medico.numero_albo = numero_albo
        if specialita_ids is not None:
            medico.specialita = self._risolvi_specialita(specialita_ids)

        return self.medico_repository.update(medico)

    def delete(self, medico_id: int) -> None:
        medico = self.medico_repository.get_by_id(medico_id)
        if medico is None:
            raise LookupError("Medico non trovato")
        utente_id = medico.utente_id
        self.medico_repository.delete(medico_id)
        self.utente_repository.delete(utente_id)
