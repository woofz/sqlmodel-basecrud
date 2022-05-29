# SQLModel BaseCRUD
###### *Simple package that provides base CRUD operations for your models.*

### What is SQLModel BaseCRUD?
With SQLModel BaseCRUD, you can implement your CRUD operation easily in your project. It is simple as declaring a variable!
This package consists in two classes: *BaseCRUD* and *BaseRepository*. 
**BaseCRUD** is the basic class that implements the basic CRUD operations, while **BaseRepository** is the repository used to execute those operations. You could also write your own repository class and use basic CRUD operation provided by **BaseRepository** class by extending it to your own repository class!

### Installation
##### Using pip
`pip install sqlmodel-basecrud`

##### Using poetry
`poetry add sqlmodel-basecrud`

### Operations

### Usage
##### Basic setup
Consider these two model as example:
```python
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="team")
	
	
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
```
We want to perform some operations on these models.  First of all we instantiate a *BaseRepository*, specifying the database session and the model that we want to manipulate.

```python
# other imports..
from sqlmodel-basecrud import BaseRepository

with Session(engine) as session:
	hero_repository = BaseRepository(db=session, model=Hero)
	team_repository = BaseRepository(db=session, model=Team)
```
##### CREATE operation
Persists an item into the database.
```python
# CREATE operation
my_hero = Hero(name='Github Hero', secret_name='Gitty', age=31)
hero_repository.create(my_hero)
# now my_hero is persisting in the database!
```
##### GET operation
GET operation simply gets a single record from the database.
```python
result = hero_repository.get(id=1, name='Github Hero')
```
*result* variable will be an instance of Hero, if a result matches the criteria, or None type.
##### FILTER operation
Gets one or more instances from the database, filtering them by one or more column/s.
```python
results = hero_repository.filter(age=31)
```
*results*  will be a *List* with zero or more elements.
##### GET ALL operation
Gets all instances of given module from the Database
```python
results = hero_repository.get_all()
```
*results*  will be a *List* with zero or more elements.
##### UPDATE operation
Updates a record into the database.
```python
instance_to_update = hero_repository.get(id=1)
instance_to_update.name = 'Super New Name'
instance_to_update.age = 27

hero_repository.update(instance_to_update)
```
The hero will have his columns *name *and *age* with updated values. 
##### DELETE operation
Removes an instance from the database
```python
instance_to_remove = hero_repository.get(id=1)
hero_repository.delete(instance_to_remove)
```
The instance will be removed from the database.

### Custom Repository
If you want to extend the BaseRepository class with some custom methods, you can write your own repository class. Just extend BaseRepository or BaseCRUD class and call the super class constructor, by passing it two essential parameters:
- **db**: must be a Session instance;
- **model**: must be a Type[SQLModel].

```python
from sqlmodel-basecrud import BaseRepository


class MyCustomRepository(BaseRepository):

    def __init__(self, db: Session, model: Type[SQLModel]):
        super().__init__(model, db)
```
### What's  next
The first thing that comes to my mind is to extend the features of Async to BaseCRUD class.  I will try to enhance the features of the project. Suggestions are appreciated 🤩

### Inspired by
- *FastAPI*: framework, high performance, easy to learn, fast to code, ready for production

- *SQLModel*, SQL databases in Python, designed for simplicity, compatibility, and robustness.