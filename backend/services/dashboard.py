from datetime import date

from sqlalchemy.orm import Session

from repositories.pagamento import PagamentoRepository


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.pagamento_repository = PagamentoRepository(db)

    def kpi(self, da: date | None, a: date | None) -> dict:
        incasso_totale = self.pagamento_repository.sum_by_periodo(da, a)
        numero_prestazioni = self.pagamento_repository.count_by_periodo(da, a)
        if numero_prestazioni > 0:
            ticket_medio = incasso_totale / numero_prestazioni
        else:
            ticket_medio = 0.0
        return {
            "incasso_totale": round(incasso_totale, 2),
            "numero_prestazioni": numero_prestazioni,
            "ticket_medio": round(ticket_medio, 2),
        }

    def incassi(self, da: date | None, a: date | None, raggruppa: str) -> list[dict]:
        if raggruppa == "specialita":
            righe = self.pagamento_repository.group_by_specialita(da, a)
        elif raggruppa == "sede":
            righe = self.pagamento_repository.group_by_sede(da, a)
        elif raggruppa == "mese":
            righe = self.pagamento_repository.group_by_mese(da, a)
        else:
            raise ValueError("Raggruppamento non valido")

        risultato = []
        for etichetta, totale in righe:
            risultato.append({"etichetta": etichetta, "totale": totale})
        return risultato

    def prestazioni(self, da: date | None, a: date | None) -> list[dict]:
        righe = self.pagamento_repository.group_by_prestazione(da, a)
        risultato = []
        for prestazione_id, nome, numero, incasso in righe:
            risultato.append(
                {
                    "prestazione_id": prestazione_id,
                    "nome": nome,
                    "numero": numero,
                    "incasso": incasso,
                }
            )
        return risultato
