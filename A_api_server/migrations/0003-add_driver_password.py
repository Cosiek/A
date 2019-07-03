#!/usr/bin/env python
# encoding: utf-8

from db import engine
from migrator import BaseMigration
from models import Driver


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0002-firm_vehicle_of_device.py']

    def run(self):
        conn = engine.connect()
        sql = "ALTER TABLE {} ADD COLUMN password VARCHAR(12)"\
            .format(Driver.__tablename__)
        conn.execute(sql)
