from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UtenteCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    ruolo: str


class UtenteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    ruolo: str
    is_active: bool
    created_at: datetime
    medico_id: int | None = None
    paziente_id: int | None = None


class UtenteEditRequest(BaseModel):
    nome: str | None = None
    cognome: str | None = None
    telefono: str | None = None
    numero_albo: str | None = None
    is_active: bool | None = None


class UtenteDettaglio(BaseModel):
    id: int
    email: EmailStr
    ruolo: str
    is_active: bool
    created_at: datetime
    nome: str | None = None
    cognome: str | None = None
    telefono: str | None = None
    codice_fiscale: str | None = None
    numero_albo: str | None = None
