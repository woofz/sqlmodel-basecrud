from typing import TypeVar, Type, Optional, List, Any

from sqlalchemy.sql.elements import BinaryExpression
from sqlmodel import Session, SQLModel, select

# Workaround for SQLAlchemy Warning
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

ModelClass = TypeVar('ModelClass', bound=SQLModel)


class BaseCRUD:
    """Simple class providing base CRUD operations on given Model"""
    db: Session
    model: Type[ModelClass]

    def __init__(self, model: Type[ModelClass], db: Session):
        """
        Class constructor
        Args:
            model: The model onto perform operations
            db: Database engine Session
        """
        self.model = model
        self.db = db

    def create(self, instance: SQLModel) -> Optional[SQLModel]:
        """
        Persists an item into the Database
        Args:
            instance: model to persist

        Returns:
            Optional[SQLModel]: the created instance itself

        """
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get(self, *args: BinaryExpression, **kwargs: Any) -> Optional[ModelClass]:
        """
        Gets a single record from the database
        Args:
            *args: filter args
            **kwargs: filter args

        Returns:
            Optional[ModelClass]: the retrieved instance or None

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
        Args:
            offset: specifies the point from where to start returning data
            limit: parameter that limits the number of results
            *args: filter args
            **kwargs: filter args

        Returns:
            List: List of retrieved items from the database

        """
        result = self.db.execute(select(self.model).filter(*args).filter_by(**kwargs).offset(offset).limit(limit))
        return result.scalars().all()

    def get_all(self) -> Optional[List[ModelClass]]:
        """
        Gets all instances of given module from the Database
        Returns:
            List: List of all instances of that model in the database.
        """
        statement = select(self.model)
        return self.db.exec(statement).all()

    def update(self, instance: SQLModel) -> ModelClass:
        """
        Updates a record into database. It is equal to create data process, so it will call that method
        Args:
            instance: the instance to update

        Returns:
            ModelClass: the updated instance
        """
        updated_instance = self.create(instance)
        return updated_instance

    def delete(self, instance: Type[ModelClass]) -> ModelClass:
        """
        Removes an instance from the database
        Args:
            instance: the instance to remove

        Returns:
            ModelClass: the instance removed
        """
        self.db.delete(instance)
        self.db.commit()
        return instance
