from sqlalchemy.orm import Session

from models.sede import Sede
from repositories.base import BaseRepository


class SedeRepository(BaseRepository[Sede]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Sede)
