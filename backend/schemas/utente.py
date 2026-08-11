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
