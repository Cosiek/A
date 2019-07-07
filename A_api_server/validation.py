#!/usr/bin/env python
# encoding: utf-8

import hashlib
import hmac
import json

from models import Device
from settings import OBSCURATION_KEY


def get_signature(params, key):
    # prepare data
    data = params.copy()
    del data['signature']
    dt = ""
    # dict fails as it might alter keys ordering
    for k in sorted(data.keys()):
        dt += str(k) + str(data[k])
    # calculate signature
    # TODO: use OpenSSL
    m = hmac.new(key.encode('utf-8'), dt.encode('utf-8'), hashlib.md5)
    return m.hexdigest()


async def validate(request, session, required_params=None):
    required_params = set(required_params or [])
    required_params.update(['id', 'signature', 'timestamp'])
    try:
        params = json.loads(await request.text())
    except json.decoder.JSONDecodeError:
        # invalid data
        return False, {'text': "Bad Request", 'status': 400}, None, None

    for param_name in required_params:
        if params.get(param_name) is None:
            return False, {'text': "Bad Request", 'status': 400}, None, None

    # TODO: use real (db) device id instead of a name
    device_id = params.get("id")
    device_signature = params.get("signature")
    device_timestamp = params.get("timestamp")

    if not (isinstance(device_timestamp, int)
            or device_timestamp < 1560893551960):
        return False, {'text': "Bad Request", 'status': 400}, None, None

    # get device data from db
    device = session.query(Device)\
            .filter_by(name=device_id, is_active=True).first()
    if device is None:
        return (False,
                {'text': "Błędny identyfikator urządzenia.", 'status': 404},
                None, None)

    # check if incoming timestamp is later then last received one
    if device.timestamp >= device_timestamp:
        return False, {'text': "Bad Request", 'status': 400}, None, None

    # generate signature based on passed data
    local_signature = get_signature(params, device.key)

    # compare signatures
    if device_signature == local_signature:
        return True, {'text': "Ok", 'status': 200}, device, params
    else:
        return (False, {'text': "Zły podpis wiadomośći.", 'status': 401},
                device, params)


def view_validation(required_params=None, update_t=True):
    """
    A decorator that validates if incoming requests are properly signed and
    have correct timestamp.

    Since it needs to parse incoming json and get device from db, it also
    annotates requests with this data.

    :param required_params: list of keys that should be present in passed json
    :param update_t: whether or not to update device timestamp id db.
    """
    def outer_wrapper(f):
        async def inner_wrapper(request):
            # run validation
            is_valid, response_kwargs, device, params = await validate(
                request, request['db_session'], required_params)
            # update timestamp if valid
            if is_valid and update_t:
                device.timestamp = params["timestamp"]
            # pass everything to request
            request['is_valid'] = is_valid
            request['response_kwargs'] = response_kwargs
            request['device'] = device
            request['params'] = params
            # run view
            return await f(request)
        return inner_wrapper
    return outer_wrapper


def obscure(password):
    m = hmac.new(OBSCURATION_KEY, password.encode('utf-8'), hashlib.md5)
    return m.hexdigest()
