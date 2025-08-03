from sqlalchemy import Integer, String, ForeignKey, Text, BIGINT, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dp.config import Base, DB, CRUD

engine = DB.engine


class User(Base, CRUD):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(100), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=True)
    city = relationship("City", back_populates="users", lazy='selectin')
    chat = relationship('Chat', back_populates='user')
    username: Mapped[str] = mapped_column(String(100), nullable=False)

    def __str__(self):
        return self.name


class City(Base, CRUD):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    users = relationship("User", back_populates="city")


class Chat(Base, CRUD):
    __tablename__ = 'chats'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_1_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    chat_2_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    users_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='chat')


class Message(Base, CRUD):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    from_chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    to_chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    message_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())


class Channel(Base, CRUD):
    __tablename__ = 'channnles'
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(BIGINT)
    link: Mapped[str] = mapped_column(String(255), nullable=True, default='')


Base.metadata.create_all(engine)
metadata = Base.metadata
