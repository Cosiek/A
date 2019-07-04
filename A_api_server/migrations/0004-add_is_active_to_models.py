#!/usr/bin/env python
# encoding: utf-8

from db import engine
from migrator import BaseMigration
from models import Device, Driver, Firm, Vehicle


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0003-add_driver_password.py']

    def run(self):
        sql = "ALTER TABLE {} ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"
        conn = engine.connect()
        conn.execute(sql.format(Device.__tablename__))
        conn.execute(sql.format(Driver.__tablename__))
        conn.execute(sql.format(Firm.__tablename__))
        conn.execute(sql.format(Vehicle.__tablename__))
