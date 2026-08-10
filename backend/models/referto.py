from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Referto(Base):
    __tablename__ = "referti"

    id: Mapped[int] = mapped_column(primary_key=True)
    appuntamento_id: Mapped[int] = mapped_column(
        ForeignKey("appuntamenti.id"), unique=True, nullable=False
    )
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    descrizione: Mapped[str | None] = mapped_column(String)

    appuntamento: Mapped["Appuntamento"] = relationship(back_populates="referto")
