#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Integer, String

from db import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(13), unique=True)
    key = Column(String(32))
    timestamp = Column(Integer)
