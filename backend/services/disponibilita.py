from datetime import date, time

from sqlalchemy.orm import Session

from models import Disponibilita
from repositories.disponibilita import DisponibilitaRepository
from repositories.sede import SedeRepository

# Stati che tengono uno slot occupato; un appuntamento annullato lo libera di nuovo
STATI_CHE_OCCUPANO_LO_SLOT = ("prenotato", "confermato", "completato")


def slot_e_libero(disponibilita: Disponibilita) -> bool:
    appuntamento = disponibilita.appuntamento
    return appuntamento is None or appuntamento.stato not in STATI_CHE_OCCUPANO_LO_SLOT


class DisponibilitaService:
    def __init__(self, db: Session) -> None:
        self.disponibilita_repository = DisponibilitaRepository(db)
        self.sede_repository = SedeRepository(db)

    def list_by_medico(self, medico_id: int) -> list[Disponibilita]:
        return self.disponibilita_repository.find_by_medico(medico_id)

    def list_libere(
        self, medico_id: int | None = None, sede_id: int | None = None
    ) -> list[Disponibilita]:
        return self.disponibilita_repository.find_libere(medico_id, sede_id)

    def create(
        self, medico_id: int, sede_id: int, data: date, ora_inizio: time, ora_fine: time
    ) -> Disponibilita:
        if self.sede_repository.get_by_id(sede_id) is None:
            raise LookupError("Sede non trovata")
        if ora_fine <= ora_inizio:
            raise ValueError("L'ora di fine deve essere successiva all'ora di inizio")

        disponibilita = Disponibilita(
            medico_id=medico_id,
            sede_id=sede_id,
            data=data,
            ora_inizio=ora_inizio,
            ora_fine=ora_fine,
        )
        return self.disponibilita_repository.create(disponibilita)

    def update(
        self,
        disponibilita_id: int,
        richiedente_medico_id: int | None,
        sede_id: int | None = None,
        data: date | None = None,
        ora_inizio: time | None = None,
        ora_fine: time | None = None,
    ) -> Disponibilita:
        disponibilita = self.disponibilita_repository.get_by_id(disponibilita_id)
        if disponibilita is None:
            raise LookupError("Disponibilita non trovata")
        if richiedente_medico_id is not None and disponibilita.medico_id != richiedente_medico_id:
            raise PermissionError("Non puoi modificare la disponibilita di un altro medico")
        if not slot_e_libero(disponibilita):
            raise ValueError("Lo slot è già prenotato")

        if sede_id is not None:
            if self.sede_repository.get_by_id(sede_id) is None:
                raise LookupError("Sede non trovata")
            disponibilita.sede_id = sede_id
        if data is not None:
            disponibilita.data = data
        if ora_inizio is not None:
            disponibilita.ora_inizio = ora_inizio
        if ora_fine is not None:
            disponibilita.ora_fine = ora_fine
        if disponibilita.ora_fine <= disponibilita.ora_inizio:
            raise ValueError("L'ora di fine deve essere successiva all'ora di inizio")

        return self.disponibilita_repository.update(disponibilita)

    def delete(self, disponibilita_id: int, richiedente_medico_id: int | None) -> None:
        disponibilita = self.disponibilita_repository.get_by_id(disponibilita_id)
        if disponibilita is None:
            raise LookupError("Disponibilita non trovata")
        if richiedente_medico_id is not None and disponibilita.medico_id != richiedente_medico_id:
            raise PermissionError("Non puoi eliminare la disponibilita di un altro medico")
        # Eliminare la riga (non solo modificarla) e' permesso solo se non e' mai stata
        # prenotata: se esiste un appuntamento, anche annullato, va conservato come storico.
        if disponibilita.appuntamento is not None:
            raise ValueError(
                "Non è possibile eliminare uno slot già prenotato in passato, anche se annullato"
            )

        self.disponibilita_repository.delete(disponibilita_id)
