from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from src.db.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(100), nullable=False)
    token = Column(String(100), unique=True)


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    owner = Column(ForeignKey('user.id'))
