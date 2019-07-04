#!/usr/bin/env python
# encoding: utf-8

from db import engine
from migrator import BaseMigration
from models import Vehicle


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0004-add_is_active_to_models.py']

    def run(self):
        conn = engine.connect()
        sql = "ALTER TABLE {} ADD COLUMN " \
              "firm_id INTEGER REFERENCES firms(id)" \
            .format(Vehicle.__tablename__)
        conn.execute(sql)
