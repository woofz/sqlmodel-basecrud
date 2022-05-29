from typing import Type

from sqlmodel import Session, SQLModel

from basecrud import BaseCRUD


class BaseRepository(BaseCRUD):

    def __init__(self, db: Session, model: Type[SQLModel]):
        super().__init__(model, db)
