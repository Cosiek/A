#!/usr/bin/env python
# encoding: utf-8

from geoalchemy2.types import Geography
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base
from enums import TransportModeEnum


class OrganizerStation(Base):
    __tablename__ = 'organizer_stations'

    name = Column(String(64), unique=False, nullable=True)
    organizer_id = Column(Integer, ForeignKey('organizers.id'), primary_key=True)
    station_id = Column(Integer, ForeignKey('stations.id'), primary_key=True)


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)

    organizers = relationship("Organizer", secondary="organizer_stations",
                              back_populates='stations')
    platforms = relationship("Platform", back_populates='station')


class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    mode = Column(Enum(TransportModeEnum), nullable=False)
    location = Column(Geography(geometry_type='POINT'))

    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station = relationship("Station", back_populates="platforms")

    outgoing = relationship("Section", back_populates="start_platform",
                            foreign_keys='Section.start_platform_id')
    incoming = relationship("Section", back_populates="end_platform",
                            foreign_keys='Section.end_platform_id')


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    mode = Column(Enum(TransportModeEnum), nullable=False)

    start_platform_id = Column(Integer, ForeignKey('platforms.id'),
                               nullable=False)
    start_platform = relationship("Platform", back_populates="outgoing",
                                  foreign_keys=[start_platform_id])

    end_platform_id = Column(Integer, ForeignKey('platforms.id'),
                             nullable=False)
    end_platform = relationship("Platform", back_populates="incoming",
                                foreign_keys=[end_platform_id])

    routes = relationship('Route', secondary='route_sections',
                          back_populates='sections')
    drives = relationship('Drive', back_populates='section')
