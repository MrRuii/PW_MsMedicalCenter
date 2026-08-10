from datetime import date, time

from sqlalchemy import Date, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Disponibilita(Base):
    __tablename__ = "disponibilita"

    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medici.id"), nullable=False)
    sede_id: Mapped[int] = mapped_column(ForeignKey("sedi.id"), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    ora_inizio: Mapped[time] = mapped_column(Time, nullable=False)
    ora_fine: Mapped[time] = mapped_column(Time, nullable=False)

    medico: Mapped["Medico"] = relationship(back_populates="disponibilita")
    sede: Mapped["Sede"] = relationship(back_populates="disponibilita")
    appuntamento: Mapped["Appuntamento"] = relationship(
        back_populates="disponibilita", uselist=False
    )
