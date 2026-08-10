from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Sede(Base):
    __tablename__ = "sedi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    citta: Mapped[str] = mapped_column(String, nullable=False)
    indirizzo: Mapped[str] = mapped_column(String, nullable=False)

    disponibilita: Mapped[list["Disponibilita"]] = relationship(back_populates="sede")
    appuntamenti: Mapped[list["Appuntamento"]] = relationship(back_populates="sede")
