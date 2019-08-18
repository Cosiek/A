#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, join, realpath
import sys

import docker

_current_dir = dirname(realpath(__file__))
client = docker.from_env()


class Container:
    name = 'spatial_db'
    image = 'mdillon/postgis'
    volumes = {
        join(_current_dir, 'socket'): {'bind': '/var/run/postgresql', 'mode': 'rw'},
    }
    socket = join(_current_dir, 'socket')
    env = {
        'POSTGRES_USER': 'postgres',
        'POSTGRES_DB': 'postgres',
        'POSTGRES_PASSWORD': 'pass',  # TODO: manage this properly
        #'POSTGRES_PORT_5432_TCP_ADDR': '',
        #'POSTGRES_PORT_5432_TCP_PORT': '',
        #'PGDATA': '',
        #'POSTGRES_INITDB_WALDIR': '',
    }

    def __getitem__(self, item):
        return self.env[item]

    def start(self):
        if self.is_running():
            return

        try:
            container = self.get_container()
            container.start()
        except docker.errors.NotFound:
            client.containers.run(self.image, environment=self.env, detach=True,
                                  name=self.name, volumes=self.volumes)

    def stop(self):
        if self.is_running():
            self.get_container().stop()

    def create(self):
        container = self.get_container()
        container.exec_run('createdb {}'.format(self.env['POSTGRES_DB']),
                           user=self.env['POSTGRES_USER'])
        # add postGIS
        container.exec_run('psql -c "CREATE EXTENSION Postgis;"',
                           user=self.env['POSTGRES_USER'])

    def drop(self):
        container = self.get_container()
        container.exec_run("dropdb {}".format(self.env['POSTGRES_DB']),
                           user=self.env['POSTGRES_USER'])

    def is_running(self):
        try:
            container = self.get_container()
        except docker.errors.NotFound:
            return False
        return container.status == 'running'

    def get_container(self):
        return client.containers.get(self.name)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'start'

    c = Container()
    f = getattr(c, cmd)
    f()
