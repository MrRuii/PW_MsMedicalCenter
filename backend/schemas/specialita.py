from pydantic import BaseModel, ConfigDict


class SpecialitaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descrizione: str | None
