from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


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
