from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Appuntamento(Base):
    __tablename__ = "appuntamenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    paziente_id: Mapped[int] = mapped_column(ForeignKey("pazienti.id"), nullable=False)
    disponibilita_id: Mapped[int] = mapped_column(
        ForeignKey("disponibilita.id"), nullable=False
    )
    prestazione_id: Mapped[int] = mapped_column(
        ForeignKey("prestazioni.id"), nullable=False
    )
    medico_id: Mapped[int] = mapped_column(ForeignKey("medici.id"), nullable=False)
    sede_id: Mapped[int] = mapped_column(ForeignKey("sedi.id"), nullable=False)
    data_ora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    stato: Mapped[str] = mapped_column(
        String, nullable=False, comment="prenotato | confermato | annullato | completato"
    )
    created_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())

    paziente: Mapped["Paziente"] = relationship(back_populates="appuntamenti")
    disponibilita: Mapped["Disponibilita"] = relationship(back_populates="appuntamento")
    prestazione: Mapped["Prestazione"] = relationship(back_populates="appuntamenti")
    medico: Mapped["Medico"] = relationship(back_populates="appuntamenti")
    sede: Mapped["Sede"] = relationship(back_populates="appuntamenti")
    pagamento: Mapped["Pagamento"] = relationship(back_populates="appuntamento", uselist=False)
    referto: Mapped["Referto"] = relationship(back_populates="appuntamento", uselist=False)
