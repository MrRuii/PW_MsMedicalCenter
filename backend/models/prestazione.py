from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Prestazione(Base):
    __tablename__ = "prestazioni"

    id: Mapped[int] = mapped_column(primary_key=True)
    specialita_id: Mapped[int] = mapped_column(ForeignKey("specialita.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    durata_min: Mapped[int] = mapped_column(nullable=False)
    prezzo: Mapped[float] = mapped_column(Numeric, nullable=False)

    specialita: Mapped["Specialita"] = relationship(back_populates="prestazioni")
    appuntamenti: Mapped[list["Appuntamento"]] = relationship(back_populates="prestazione")
