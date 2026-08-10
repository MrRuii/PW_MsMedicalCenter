from sqlalchemy import Column, ForeignKey, Table

from core.database import Base

medico_specialita = Table(
    "medici_specialita",
    Base.metadata,
    Column("medico_id", ForeignKey("medici.id"), primary_key=True),
    Column("specialita_id", ForeignKey("specialita.id"), primary_key=True),
)
