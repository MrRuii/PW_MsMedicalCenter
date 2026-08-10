from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Pagamento(Base):
    __tablename__ = "pagamenti"

    id: Mapped[int] = mapped_column(primary_key=True)
    appuntamento_id: Mapped[int] = mapped_column(
        ForeignKey("appuntamenti.id"), unique=True, nullable=False
    )
    importo: Mapped[float] = mapped_column(Numeric, nullable=False)
    data: Mapped[date | None] = mapped_column(Date)
    stato: Mapped[str] = mapped_column(
        String, nullable=False, comment="in attesa | pagato | rimborsato"
    )

    appuntamento: Mapped["Appuntamento"] = relationship(back_populates="pagamento")
