from sqlalchemy.orm import Session

from models.specialita import Specialita
from repositories.base import BaseRepository


class SpecialitaRepository(BaseRepository[Specialita]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Specialita)
