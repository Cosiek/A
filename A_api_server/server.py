#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.get('/', hello)])

    web.run_app(app)
