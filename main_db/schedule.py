#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import (Column, Enum, ForeignKey,
                        Integer, SmallInteger, String, Time)
from sqlalchemy.orm import relationship

from db import Base
from enums import TransportModeEnum


class Line(Base):
    __tablename__ = 'lines'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)
    mode = Column(Enum(TransportModeEnum), nullable=False)

    organizer_id = Column(Integer, ForeignKey('organizers.id'))
    organizer = relationship('Organizer', back_populates='lines')

    brigades = relationship('Brigade', back_populates='line')


class Brigade(Base):
    __tablename__ = 'brigades'

    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=False, nullable=False)

    line_id = Column(Integer, ForeignKey('lines.id'))
    line = relationship('Line', back_populates='brigades')

    half_runs = relationship('HalfRun', back_populates='brigade')
    schedules = relationship('Schedule', secondary='schedule_brigades',
                             back_populates='brigades')


class HalfRun(Base):
    __tablename__ = 'half_runs'

    order = Column(SmallInteger)

    id = Column(Integer, primary_key=True)

    brigade_id = Column(Integer, ForeignKey('brigades.id'))
    brigade = relationship('Brigade', back_populates='half_runs')

    drives = relationship("Drive", back_populates='half_run')

    route_id = Column(Integer, ForeignKey('routes.id'))
    route = relationship('Route', back_populates='half_runs')


class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)

    half_runs = relationship('HalfRun', back_populates='route')
    sections = relationship('Section', secondary='route_sections',
                            back_populates='routes')


class RouteSection(Base):
    __tablename__ = 'route_sections'

    route_id = Column(Integer, ForeignKey('routes.id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id'), primary_key=True)
    ordinal_number = Column(Integer, primary_key=True)


class Drive(Base):
    __tablename__ = 'drives'

    id = Column(Integer, primary_key=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    half_run_id = Column(Integer, ForeignKey('half_runs.id'))
    half_run = relationship("HalfRun", back_populates='drives')

    section_id = Column(Integer, ForeignKey('sections.id'))
    section = relationship("Section", back_populates="drives")


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)

    days = relationship('Day', secondary='schedule_days',
                        back_populates='schedules')
    brigades = relationship('Brigade', secondary='schedule_brigades',
                            back_populates='schedules')


class ScheduleDay(Base):
    __tablename__ = 'schedule_days'

    day_id = Column(Integer, ForeignKey('calendar.id'), primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'), primary_key=True)


class ScheduleBrigade(Base):
    __tablename__ = 'schedule_brigades'

    schedule_id = Column(Integer, ForeignKey('schedules.id'), primary_key=True)
    brigade_id = Column(Integer, ForeignKey('brigades.id'), primary_key=True)
