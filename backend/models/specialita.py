from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.medico_specialita import medico_specialita


class Specialita(Base):
    __tablename__ = "specialita"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descrizione: Mapped[str | None] = mapped_column(String)

    prestazioni: Mapped[list["Prestazione"]] = relationship(back_populates="specialita")
    medici: Mapped[list["Medico"]] = relationship(
        secondary=medico_specialita, back_populates="specialita"
    )
