from typing import TypeVar, Type, Optional, List, Any

from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import Session, SQLModel, select

# Workaround for SQLAlchemy Warning
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

ModelClass = TypeVar('ModelClass', bound=SQLModel)


class BaseCRUD:
    db: Session
    model: Type[ModelClass]

    def __init__(self, model: Type[ModelClass], db: Session):
        """
        Simple class providing base CRUD operations on given Model
        :param model: The model onto perform operations
        :param db: Database engine Session
        """
        self.model = model
        self.db = db

    def create(self, instance: SQLModel) -> Optional[SQLModel]:
        """
        Persists an item into the Database
        :param instance: model to persist
        :return: the created instance itself
        """
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, *args: BinaryExpression, **kwargs: Any) -> Optional[ModelClass]:
        """
        Gets a single record from the database
        :param args: filter args
        :param kwargs: filter args
        :return:
        """
        statement = select(self.model).filter(*args).filter_by(**kwargs)
        return self.db.exec(statement).first()

    def filter(self,
               offset: Optional[int] = 0,
               limit: Optional[int] = 100,
               *args: BinaryExpression,
               **kwargs: Any) -> List[Any]:
        """
        Gets one or more instances from the database, filtering them by one or more column
        :param offset: specifies the point from where to start returning data
        :param limit: parameter that limits the number of results
        :param args: filter args
        :param kwargs: filter args
        :return: List of retrieved items from the database
        """
        result = self.db.execute(select(self.model).filter(*args).filter_by(**kwargs).offset(offset).limit(limit))
        return result.scalars().all()

    def get_all(self) -> Optional[List[ModelClass]]:
        """
        Gets all instances of given module from the Database
        :return:
        """
        statement = select(self.model)
        return self.db.exec(statement).all()

    def update(self, instance: SQLModel) -> ModelClass:
        """
        Updates a record into database. It is equal to create data process, so it will call that method
        :param instance: the instance to update
        :return: the updated instance
        """
        updated_instance = self.create(instance)
        return updated_instance

    def delete(self, instance: Type[ModelClass]) -> ModelClass:
        """
        Removes an instance from the database
        :param instance: the instance to remove
        :return: the instance removed
        """
        self.db.delete(instance)
        self.db.commit()
        return instance
