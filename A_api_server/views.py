#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web

from validation import validate


async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    is_valid, response_kwargs, _ = await validate(request)
    return web.Response(**response_kwargs)
