from typing import Type

from sqlmodel import Session, SQLModel

from .basecrud import BaseCRUD


class BaseRepository(BaseCRUD):
    """Base class for CRUD Operations"""
    def __init__(self, db: Session, model: Type[SQLModel]):
        """
        Constructor
        Args:
            db: the database session
            model: the model class that should be manipulated
        """
        super().__init__(model, db)
