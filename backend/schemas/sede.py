from pydantic import BaseModel, ConfigDict


class SedeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    citta: str
    indirizzo: str


class SedeCreate(BaseModel):
    nome: str
    citta: str
    indirizzo: str


class SedeUpdate(BaseModel):
    nome: str | None = None
    citta: str | None = None
    indirizzo: str | None = None
