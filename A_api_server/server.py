#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web

import views


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.post('/device/register', views.device_register),
        web.post('/drivers', views.drivers),
        web.post('/driver/login', views.driver_login),
        web.post('/driver/logout', views.driver_logout),
        web.post('/lines', views.lines),
        web.post('/line/brigades', views.brigades),
        web.post('/driver/start_task', views.start_task),
    ])

    web.run_app(app)
