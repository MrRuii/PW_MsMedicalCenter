from datetime import date

from sqlalchemy.orm import Session

from models import Pagamento
from repositories.appuntamento import AppuntamentoRepository
from repositories.pagamento import PagamentoRepository


class PagamentoService:
    def __init__(self, db: Session) -> None:
        self.pagamento_repository = PagamentoRepository(db)
        self.appuntamento_repository = AppuntamentoRepository(db)

    def registra_incasso(self, appuntamento_id: int, importo: float | None) -> Pagamento:
        appuntamento = self.appuntamento_repository.get_by_id(appuntamento_id)
        if appuntamento is None:
            raise LookupError("Appuntamento non trovato")
        if appuntamento.stato != "completato":
            raise ValueError("Il pagamento può essere registrato solo su un appuntamento completato")
        if self.pagamento_repository.find_by_appuntamento(appuntamento_id) is not None:
            raise ValueError("Questo appuntamento ha già un pagamento registrato")

        pagamento = Pagamento(
            appuntamento_id=appuntamento_id,
            importo=importo if importo is not None else float(appuntamento.prestazione.prezzo),
            data=date.today(),
            stato="pagato",
        )
        return self.pagamento_repository.create(pagamento)

    def lista_filtrata(
        self, da: date | None, a: date | None, stato: str | None
    ) -> list[Pagamento]:
        return self.pagamento_repository.find_filtrati(da, a, stato)

    def rimborsa(self, pagamento_id: int) -> Pagamento:
        pagamento = self.pagamento_repository.get_by_id(pagamento_id)
        if pagamento is None:
            raise LookupError("Pagamento non trovato")
        if pagamento.stato != "pagato":
            raise ValueError("Solo un pagamento con stato 'pagato' può essere rimborsato")
        pagamento.stato = "rimborsato"
        return self.pagamento_repository.update(pagamento)
