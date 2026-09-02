from datetime import date

from sqlalchemy.orm import Session

from core.file_storage import FileStorage
from models import Referto, Utente
from repositories.appuntamento import AppuntamentoRepository
from repositories.referto import RefertoRepository


class RefertoService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.referto_repository = RefertoRepository(db)
        self.appuntamento_repository = AppuntamentoRepository(db)
        self.file_storage = FileStorage()

    def verifica_accesso(self, utente: Utente, referto: Referto) -> bool:
        if utente.ruolo == "admin":
            return True
        appuntamento = referto.appuntamento
        if utente.paziente is not None and appuntamento.paziente_id == utente.paziente.id:
            return True
        if utente.medico is not None and appuntamento.medico_id == utente.medico.id:
            return True
        return False

    def list_per_utente(self, utente: Utente) -> list[Referto]:
        if utente.ruolo == "admin":
            return self.referto_repository.get_all()
        if utente.ruolo == "medico" and utente.medico is not None:
            return self.referto_repository.find_by_medico(utente.medico.id)
        if utente.ruolo == "paziente" and utente.paziente is not None:
            return self.referto_repository.find_by_paziente(utente.paziente.id)
        return []

    def carica(
        self,
        appuntamento_id: int,
        richiedente_medico_id: int | None,
        content_type: str | None,
        contenuto: bytes,
        descrizione: str | None,
    ) -> Referto:
        appuntamento = self.appuntamento_repository.get_by_id(appuntamento_id)
        if appuntamento is None:
            raise LookupError("Appuntamento non trovato")
        if richiedente_medico_id is not None and appuntamento.medico_id != richiedente_medico_id:
            raise PermissionError("Non puoi caricare un referto per un appuntamento di un altro medico")
        if appuntamento.stato != "completato":
            raise ValueError("Il referto può essere caricato solo su un appuntamento completato")
        if appuntamento.referto is not None:
            raise ValueError("Questo appuntamento ha già un referto")

        self.file_storage.valida(content_type, len(contenuto))
        percorso = self.file_storage.salva(content_type, contenuto)

        referto = Referto(
            appuntamento_id=appuntamento_id,
            file_path=percorso,
            data=date.today(),
            descrizione=descrizione,
        )
        return self.referto_repository.create(referto)

    def aggiorna_descrizione(
        self, referto_id: int, richiedente_medico_id: int | None, descrizione: str | None
    ) -> Referto:
        referto = self.referto_repository.get_by_id(referto_id)
        if referto is None:
            raise LookupError("Referto non trovato")
        if richiedente_medico_id is not None and referto.appuntamento.medico_id != richiedente_medico_id:
            raise PermissionError("Non puoi modificare un referto di un altro medico")
        referto.descrizione = descrizione
        return self.referto_repository.update(referto)

    def elimina(self, referto_id: int, richiedente_medico_id: int | None) -> None:
        referto = self.referto_repository.get_by_id(referto_id)
        if referto is None:
            raise LookupError("Referto non trovato")
        if richiedente_medico_id is not None and referto.appuntamento.medico_id != richiedente_medico_id:
            raise PermissionError("Non puoi eliminare un referto di un altro medico")
        self.file_storage.elimina(referto.file_path)
        self.referto_repository.delete(referto_id)
