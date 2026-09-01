from pydantic import BaseModel, ConfigDict, EmailStr, Field

from schemas.specialita import SpecialitaRead


class MedicoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    cognome: str
    numero_albo: str | None
    specialita: list[SpecialitaRead] = []


class MedicoCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nome: str
    cognome: str
    numero_albo: str | None = None
    specialita_ids: list[int] = []


class MedicoUpdate(BaseModel):
    nome: str | None = None
    cognome: str | None = None
    numero_albo: str | None = None
    specialita_ids: list[int] | None = None
