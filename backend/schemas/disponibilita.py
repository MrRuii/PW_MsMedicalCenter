from datetime import date, time

from pydantic import BaseModel


class DisponibilitaRead(BaseModel):
    id: int
    medico_id: int
    sede_id: int
    data: date
    ora_inizio: time
    ora_fine: time
    libera: bool


class DisponibilitaCreate(BaseModel):
    sede_id: int
    data: date
    ora_inizio: time
    ora_fine: time


class DisponibilitaUpdate(BaseModel):
    sede_id: int | None = None
    data: date | None = None
    ora_inizio: time | None = None
    ora_fine: time | None = None
