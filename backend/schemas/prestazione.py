from pydantic import BaseModel, ConfigDict, Field


class PrestazioneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    specialita_id: int
    nome: str
    durata_min: int
    prezzo: float


class PrestazioneCreate(BaseModel):
    specialita_id: int
    nome: str
    durata_min: int = Field(gt=0)
    prezzo: float = Field(gt=0)


class PrestazioneUpdate(BaseModel):
    specialita_id: int | None = None
    nome: str | None = None
    durata_min: int | None = Field(default=None, gt=0)
    prezzo: float | None = Field(default=None, gt=0)
