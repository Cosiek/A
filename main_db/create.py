#!/usr/bin/env python
# encoding: utf-8

from db import engine, metadata

# importing table classes
import calendar
import events
import infrastructure
import organization
import schedule


if __name__ == "__main__":
    print("Create tables")
    metadata.create_all(engine)
    print("Populate calendar")
    calendar.populate_calendar(366 * 4)
