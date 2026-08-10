from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Paziente(Base):
    __tablename__ = "pazienti"

    id: Mapped[int] = mapped_column(primary_key=True)
    utente_id: Mapped[int] = mapped_column(
        ForeignKey("utenti.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String, nullable=False)
    cognome: Mapped[str] = mapped_column(String, nullable=False)
    codice_fiscale: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    data_nascita: Mapped[date | None] = mapped_column(Date)
    telefono: Mapped[str | None] = mapped_column(String)

    utente: Mapped["Utente"] = relationship(back_populates="paziente")
    