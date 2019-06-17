#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web

import views


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.post('/device/register', views.device_register)])

    web.run_app(app)
