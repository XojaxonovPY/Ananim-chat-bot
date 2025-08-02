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
    def delete(cls, filter_colm, filter_value):
        with SessionLocal() as session:
            obj = session.query(cls).filter(filter_colm == filter_value)
            if obj:
                session.delete(obj)
                session.commit()
                return True
            return False

    @classmethod
    def get(cls, filter_column, filter_value, all=False):
        with SessionLocal() as session:
            query = session.query(cls).filter(filter_column == filter_value)
            if not query:
                return None
            if all:
                return query.all()
            return query.first()

    @classmethod
    def get_all(cls):
        with SessionLocal() as session:
            query = session.query(cls)
            if not query:
                return []
            return query.all()
