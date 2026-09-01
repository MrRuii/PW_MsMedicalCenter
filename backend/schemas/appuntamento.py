from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppuntamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paziente_id: int
    medico_id: int
    sede_id: int
    prestazione_id: int
    disponibilita_id: int
    data_ora: datetime
    stato: str
    created_at: datetime | None


class AppuntamentoCreate(BaseModel):
    disponibilita_id: int
    prestazione_id: int
