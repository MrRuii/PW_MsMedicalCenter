from typing import Generic, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

#operazioni crud di default
class BaseRepository(Generic[ModelType]):

    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        self.db = db
        self.model = model

    def get_by_id(self, id: int) -> ModelType | None:
        return self.db.get(self.model, id)

    def get_all(self) -> list[ModelType]:
        return list(self.db.scalars(select(self.model)))

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelType) -> ModelType:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
