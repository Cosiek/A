#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = 'sqlite:///main.db'

engine = create_engine(DB_URL)

Base = declarative_base()

metadata = Base.metadata

Session = sessionmaker(bind=engine)
