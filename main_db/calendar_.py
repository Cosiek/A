#!/usr/bin/env python
# encoding: utf-8

from datetime import date, timedelta

from sqlalchemy import Boolean, Column, Integer, SmallInteger, Date
from sqlalchemy.orm import relationship

from db import Base, Session


INITIAL_DATE = date(2019, 7, 1)
ONE_DAY = timedelta(days=1)
HOLIDAYS = [
    (1, 1),    # new year
    (6, 1),    # three kings
    (1, 5),    # international labour day
    (3, 5),    # 3-rd of may constitution
    (15, 9),   # polish military day
    (1, 11) ,  # all saints
    (11, 11),  # independence day
    (25, 12),  # christmas
    (26, 12),  # christmas
    # moving holidays:
    # - easter (2 days)
    # - Zielone Świątki
    # - Boże Ciało
]


class Day(Base):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    weekday = Column(SmallInteger)  # 1 is monday
    is_holiday = Column(Boolean, default=False)
    is_vacation = Column(Boolean, default=False)
    # NOTE: winter vacation had different dates in different places

    schedules = relationship('Schedule', secondary='schedule_days',
                             back_populates='days')


def populate_calendar(count):
    session = Session()
    date = INITIAL_DATE
    for i in range(count):
        session.add(Day(id=i, date=date, weekday=date.weekday() + 1,
                        is_holiday=check_if_holiday(date)))
        date += ONE_DAY
    session.commit()


def check_if_holiday(date):
    for h in HOLIDAYS:
        if date.day == h[0] and date.month == h[1]:
            return True
    return False
