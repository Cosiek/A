#!/usr/bin/env python
# encoding: utf-8

from db import engine
from migrator import BaseMigration
from models import Device


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0005-add_firm_vehicle_relation.py']

    def run(self):
        conn = engine.connect()
        sql = "ALTER TABLE {} ADD COLUMN " \
              "driver_id INTEGER REFERENCES drivers(id)"\
            .format(Device.__tablename__)
        conn.execute(sql)
