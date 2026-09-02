from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.paziente import PazienteRead


class AppuntamentoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paziente_id: int
    paziente: PazienteRead
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
