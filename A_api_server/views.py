#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web

from db import Session
from validation import validate


async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    ses = Session()
    is_valid, response_kwargs, _, _ = await validate(request, ses)
    ses.close()
    return web.Response(**response_kwargs)
