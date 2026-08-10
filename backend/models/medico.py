from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.medico_specialita import medico_specialita


class Medico(Base):
    __tablename__ = "medici"

    id: Mapped[int] = mapped_column(primary_key=True)
    utente_id: Mapped[int] = mapped_column(
        ForeignKey("utenti.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    cognome: Mapped[str] = mapped_column(String, nullable=False)
    numero_albo: Mapped[str | None] = mapped_column(String, unique=True)

    utente: Mapped["Utente"] = relationship(back_populates="medico")
    specialita: Mapped[list["Specialita"]] = relationship(
        secondary=medico_specialita, back_populates="medici"
    )
    disponibilita: Mapped[list["Disponibilita"]] = relationship(back_populates="medico")
    appuntamenti: Mapped[list["Appuntamento"]] = relationship(back_populates="medico")
