import pytest
from sqlmodel import create_engine, SQLModel, Session

from sqlmodel_basecrud.baserepository import BaseRepository
from tests.data import Hero, Team


class TestBaseCRUD:
    @pytest.fixture(scope='function')
    def setup(self) -> None:
        engine = create_engine('sqlite://')
        SQLModel.metadata.create_all(engine)
        session = Session(engine)
        yield session
        session.close()

    @pytest.fixture(scope='function')
    def populate_db(self, setup):
        session = setup
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="X-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print("Updated hero:", hero_spider_boy)

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        hero_repository = BaseRepository(db=session, model=Hero)
        yield session

    def test_get(self, populate_db):
        session = populate_db
        hero_repository = BaseRepository(db=session, model=Hero)
        result = hero_repository.get(id=1, name='Deadpond')
        assert result is not None

    def test_create(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        assert team_repository.get(name='w00fz Team') is None
        team = Team(name='w00fz Team', headquarters='Amsterdam')
        team_repository.create(team)
        assert team_repository.get(name='w00fz Team') is not None

    def test_filter_empty_no_params(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        assert len(team_repository.filter(name='w00fz')) == 0

    def test_filter_full_params(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        assert len(team_repository.filter(offset=1, limit=1)) == 1

    def test_filter_params(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        res = team_repository.filter(name='Preventers', offset=0, limit=1)
        assert len(team_repository.filter(offset=0, limit=1, name='Preventers')) == 1

    def test_get_all(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        result = team_repository.get_all()
        assert len(result) == 3

    def test_delete(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        team_to_delete = team_repository.get(id=1)
        team_repository.delete(team_to_delete)
        deleted_team = team_repository.get(id=1)
        assert deleted_team is None

    def test_update(self, populate_db):
        session = populate_db
        team_repository = BaseRepository(db=session, model=Team)
        team_to_update = team_repository.get(id=1)
        old_param = team_to_update.name
        team_to_update.name = 'w00fz'
        team_repository.update(team_to_update)
        team_read_again = team_repository.get(id=1)
        assert team_read_again.name != old_param
