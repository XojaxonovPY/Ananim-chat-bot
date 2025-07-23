from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from utils.env_data import DBConfig


class Base(DeclarativeBase):
    pass


class DB:
    engine = create_engine(DBConfig.DP_URL)


engine = DB.engine

SessionLocal = sessionmaker(engine)


class CRUD:

    @classmethod
    def save(cls, **kwargs):
        with SessionLocal() as session:
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    @classmethod
    def update(cls, filter_column, filter_value, **kwargs):
        with SessionLocal() as session:
            stmt = session.query(cls).filter(filter_column == filter_value)
            stmt.update(kwargs)
            session.commit()
            return stmt.first()

    @classmethod
    def delete(cls, id):
        with SessionLocal() as session:
            obj = session.get(cls, id)
            if obj:
                session.delete(obj)
                session.commit()
                return True
            return False

    @classmethod
    def get(cls, filter_column, filter_value, one=False):
        with SessionLocal() as session:
            query = session.query(cls).filter(filter_column == filter_value)
            return query.first() if one else query.all()

    @classmethod
    def get_all(cls):
        with SessionLocal() as session:
            query = session.query(cls)
            return query.all()
