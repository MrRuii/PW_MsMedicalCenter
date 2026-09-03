from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PagamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appuntamento_id: int
    importo: float
    data: date | None
    stato: str


class PagamentoCreate(BaseModel):
    importo: float | None = Field(default=None, gt=0)
