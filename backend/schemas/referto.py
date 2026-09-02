from datetime import date

from pydantic import BaseModel, ConfigDict


class RefertoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    appuntamento_id: int
    data: date
    descrizione: str | None


class RefertoUpdate(BaseModel):
    descrizione: str | None = None
