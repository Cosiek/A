#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from db import Base
from enums import TransportModeEnum


class Line(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)

    organizer_id = Column(Integer, ForeignKey('organizers.id'))


class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)
    mode = Column(Enum(TransportModeEnum), nullable=False)

    line_id = Column(Integer, ForeignKey('lines.id'))


class Brigade(Base):
    __tablename__ = 'brigades'

    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=False, nullable=False)

    route_id = Column(Integer, ForeignKey('brigades.id'))


class Drive(Base):
    __tablename__ = 'drives'

    id = Column(Integer, primary_key=True)

    brigade_id = Column(Integer, ForeignKey('brigades.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)
