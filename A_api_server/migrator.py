#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import importlib.util
import os
from os.path import basename, join, dirname, realpath
import re

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Table
from sqlalchemy import Date, Integer, String
from sqlalchemy.sql import select


CURRENT_DIR = dirname(realpath(__file__))


class BaseMigration:
    depends_on = []
    rollback_on_error = True

    class STATUS:
        new = 0
        failed = 1
        rolled_back = 2
        reversed = 3
        done = 4

    def __init__(self, id_, name, status, finished):
        self.id_ = id_
        self.name = name
        self.status = status
        self.finished = finished

    @property
    def is_done(self):
        return self.finished is not None

    def _run(self):
        try:
            self.run()
            self.status = self.STATUS.done
            self.finished = datetime.now()
        except:
            if self.rollback_on_error:
                self.rollback()
                self.status = self.STATUS.rolled_back

    def run(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError


class Settings:

    def __init__(self):
        for k, v in self.get_default().items():
            setattr(self, k, v)

        # TODO: make this more universal
        import settings
        for k, v in settings.DATABASE.items():
            setattr(self, k, v)

    @classmethod
    def get_default(cls):
        return {
            'migrations_table_name': "migrations",
            'migration_dir': join(CURRENT_DIR, 'migrations'),
        }


class MigrationRunner:

    def __init__(self, settings):
        self.settings = settings

    def run(self):
        # connect to db(s)
        engine = create_engine(self.settings.db_url)
        metadata = MetaData(engine)
        # create migrations table (if it doesn't exist yet)
        table = self.create_migrations_table(metadata)
        # get list of migrations from db
        conn = engine.connect()
        db_migrations = {m[1]: m for m in conn.execute(select([table,]))}
        # get list of migrations from code
        code_migrations = self.get_code_migrations()
        # make instances of all migrations
        migrations = []
        for c_mi in code_migrations:
            # get migration class
            pth = join(self.settings.migration_dir, c_mi)
            spec = importlib.util.spec_from_file_location("m", pth)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            name = basename(module.__file__)  # TODO: just filename and app?

            # get initial data for migration
            db_mi = db_migrations.get(name, None)
            migration_kwargs = {
                'id_': db_mi[0] if db_mi else None,
                'name': name,
                'status': db_mi[0] if db_mi else BaseMigration.STATUS.new,
                'finished': db_mi[0] if db_mi else None,
            }

            # make migration instance
            migrations.append(module.Migration(**migration_kwargs))

        # resolve ordering
        migrations = self.sort_migrations(migrations)

        # run migrations
        for migration in migrations:
            if not migration.is_done:
                migration._run()
                # save migration run info
                self.save_migration_run_data(migration, table, conn)

    def create_migrations_table(self, metadata):
        table = Table(self.settings.migrations_table_name, metadata,
                Column('Id', Integer, primary_key=True, nullable=False),
                Column('Name', String(60)),
                Column('Status', Integer, default=BaseMigration.STATUS.new),
                Column('Finished', Date)
        )
        metadata.create_all()
        return table

    def get_code_migrations(self):
        # walk the migrations directory
        migration_files = []

        format_ = re.compile(r"^[0-9]{4}-[\w]+\.py$")
        # TODO: many migration dirs
        for filename in os.listdir(self.settings.migration_dir):
            if format_.match(filename):
                migration_files.append(filename)

        return migration_files

    @staticmethod
    def sort_migrations(migrations):
        visited = [False, ] * len(migrations)
        names = [m.name for m in migrations]
        sorted_ = []

        def ts(idx, visited, sorted_):
            visited[idx] = True

            for n in migrations[idx].depends_on:
                i = names.index(n)
                if not visited[i]:
                    ts(i, visited, sorted_)

            sorted_.append(migrations[idx])

        for idx in range(len(visited)):
            if not visited[idx]:
                ts(idx, visited, sorted_)

        return sorted_

    def save_migration_run_data(self, migration, table, conn):
        kwargs = {
            'Name': migration.name,
            'Status': migration.status,
            'Finished': migration.finished,
        }
        if migration.id_ is None:
            # new migration - never done before
            sql = table.insert().values(**kwargs)
        else:
            # updating existing migration
            sql = table.update().where(id=migration.id_).values(**kwargs)

        conn.execute(sql)


if __name__ == "__main__":
    # read config
    settings = Settings()
    # run
    runner = MigrationRunner(settings)
    runner.run()
