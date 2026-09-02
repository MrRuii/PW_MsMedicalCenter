from pydantic import BaseModel, ConfigDict


class PazienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cognome: str
    telefono: str | None
