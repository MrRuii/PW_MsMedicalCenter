from datetime import datetime

from sqlalchemy.orm import Session

from models import Appuntamento
from repositories.appuntamento import AppuntamentoRepository
from repositories.disponibilita import DisponibilitaRepository
from repositories.prestazione import PrestazioneRepository
from services.disponibilita import slot_e_libero


class SlotNonDisponibileError(Exception):
    """Sollevato quando si prova a prenotare uno slot già occupato (409)."""


class AppuntamentoService:
    def __init__(self, db: Session) -> None:
        self.appuntamento_repository = AppuntamentoRepository(db)
        self.disponibilita_repository = DisponibilitaRepository(db)
        self.prestazione_repository = PrestazioneRepository(db)

    def verifica_slot_libero(self, disponibilita) -> bool:
        return slot_e_libero(disponibilita)

    def prenota(self, paziente_id: int, disponibilita_id: int, prestazione_id: int) -> Appuntamento:
        disponibilita = self.disponibilita_repository.get_by_id(disponibilita_id)
        if disponibilita is None:
            raise LookupError("Disponibilita non trovata")

        if self.prestazione_repository.get_by_id(prestazione_id) is None:
            raise LookupError("Prestazione non trovata")

        if not self.verifica_slot_libero(disponibilita):
            raise SlotNonDisponibileError("Lo slot scelto non è più disponibile")

        data_ora = datetime.combine(disponibilita.data, disponibilita.ora_inizio)

        # Disponibilita-Appuntamento e' una relazione 1 a 1: se questo slot era stato
        # prenotato e poi annullato, la riga esiste gia' e va riusata invece di crearne
        # una seconda (violerebbe l'unicita' dello slot e il vincolo di integrita').
        appuntamento_esistente = disponibilita.appuntamento
        if appuntamento_esistente is not None:
            appuntamento_esistente.paziente_id = paziente_id
            appuntamento_esistente.prestazione_id = prestazione_id
            appuntamento_esistente.data_ora = data_ora
            appuntamento_esistente.stato = "prenotato"
            return self.appuntamento_repository.update(appuntamento_esistente)

        appuntamento = Appuntamento(
            paziente_id=paziente_id,
            disponibilita_id=disponibilita.id,
            prestazione_id=prestazione_id,
            medico_id=disponibilita.medico_id,
            sede_id=disponibilita.sede_id,
            data_ora=data_ora,
            stato="prenotato",
        )
        return self.appuntamento_repository.create(appuntamento)

    def annulla(self, appuntamento: Appuntamento) -> Appuntamento:
        if appuntamento.stato not in ("prenotato", "confermato"):
            raise ValueError("Non è possibile annullare un appuntamento in questo stato")
        appuntamento.stato = "annullato"
        return self.appuntamento_repository.update(appuntamento)

    def conferma(self, appuntamento: Appuntamento) -> Appuntamento:
        if appuntamento.stato != "prenotato":
            raise ValueError("Solo un appuntamento prenotato può essere confermato")
        appuntamento.stato = "confermato"
        return self.appuntamento_repository.update(appuntamento)

    def completa(self, appuntamento: Appuntamento) -> Appuntamento:
        if appuntamento.stato != "confermato":
            raise ValueError("Solo un appuntamento confermato può essere completato")
        appuntamento.stato = "completato"
        return self.appuntamento_repository.update(appuntamento)
