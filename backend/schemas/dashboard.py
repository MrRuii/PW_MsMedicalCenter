from pydantic import BaseModel


class DashboardKPI(BaseModel):
    incasso_totale: float
    numero_prestazioni: int
    ticket_medio: float


class IncassoRaggruppato(BaseModel):
    etichetta: str
    totale: float


class PrestazioneStat(BaseModel):
    prestazione_id: int
    nome: str
    numero: int
    incasso: float
