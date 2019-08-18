#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from db_container_handler import Container

c = Container()

DB_URL = 'postgresql+psycopg2://{}:{}@/{}?host={}'.format(
    c['POSTGRES_USER'], c['POSTGRES_PASSWORD'], c['POSTGRES_DB'], c.socket
)

engine = create_engine(DB_URL)

Base = declarative_base()

metadata = Base.metadata

Session = sessionmaker(bind=engine)
