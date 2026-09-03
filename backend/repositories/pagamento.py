from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.pagamento import Pagamento
from repositories.base import BaseRepository


class PagamentoRepository(BaseRepository[Pagamento]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Pagamento)

    def find_by_appuntamento(self, appuntamento_id: int) -> Pagamento | None:
        return self.db.scalar(
            select(Pagamento).where(Pagamento.appuntamento_id == appuntamento_id)
        )

    def find_filtrati(
        self, da: date | None = None, a: date | None = None, stato: str | None = None
    ) -> list[Pagamento]:
        query = select(Pagamento)
        if da is not None:
            query = query.where(Pagamento.data >= da)
        if a is not None:
            query = query.where(Pagamento.data <= a)
        if stato is not None:
            query = query.where(Pagamento.stato == stato)
        return list(self.db.scalars(query.order_by(Pagamento.data.desc())))

    def find_pagati(self, da: date | None, a: date | None) -> list[Pagamento]:
        return self.find_filtrati(da, a, stato="pagato")

    def sum_by_periodo(self, da: date | None, a: date | None) -> float:
        totale = 0.0
        for pagamento in self.find_pagati(da, a):
            totale += float(pagamento.importo)
        return totale

    def count_by_periodo(self, da: date | None, a: date | None) -> int:
        return len(self.find_pagati(da, a))

    def group_by_specialita(self, da: date | None, a: date | None) -> list[tuple[str, float]]:
        totali: dict[str, float] = {}
        for pagamento in self.find_pagati(da, a):
            nome = pagamento.appuntamento.prestazione.specialita.nome
            totali[nome] = totali.get(nome, 0.0) + float(pagamento.importo)
        return sorted(totali.items())

    def group_by_sede(self, da: date | None, a: date | None) -> list[tuple[str, float]]:
        totali: dict[str, float] = {}
        for pagamento in self.find_pagati(da, a):
            nome = pagamento.appuntamento.sede.nome
            totali[nome] = totali.get(nome, 0.0) + float(pagamento.importo)
        return sorted(totali.items())

    def group_by_mese(self, da: date | None, a: date | None) -> list[tuple[str, float]]:
        totali: dict[str, float] = {}
        for pagamento in self.find_pagati(da, a):
            mese = pagamento.data.strftime("%Y-%m")
            totali[mese] = totali.get(mese, 0.0) + float(pagamento.importo)
        return sorted(totali.items())

    def group_by_prestazione(self, da: date | None, a: date | None) -> list[tuple[int, str, int, float]]:
        nomi: dict[int, str] = {}
        numeri: dict[int, int] = {}
        incassi: dict[int, float] = {}
        for pagamento in self.find_pagati(da, a):
            prestazione = pagamento.appuntamento.prestazione
            nomi[prestazione.id] = prestazione.nome
            numeri[prestazione.id] = numeri.get(prestazione.id, 0) + 1
            incassi[prestazione.id] = incassi.get(prestazione.id, 0.0) + float(pagamento.importo)

        righe = [(pid, nomi[pid], numeri[pid], incassi[pid]) for pid in nomi]
        righe.sort(key=lambda riga: riga[1])
        return righe
