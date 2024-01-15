# -*- coding: utf-8 -*-
# Zilliqa Python Library
# Copyright (C) 2019  Gully Chen
# MIT License
"""
pyzil.zilliqa.api
~~~~~~~~~~~~

Json-RPC interface of Zilliqa APIs.

:copyright: (c) 2019 by Gully Chen.
:license: MIT License, see LICENSE for more details.
"""

from jsonrpcclient import Ok, request, parse
import requests

INVALID_PARAMS = "INVALID_PARAMS: Invalid method parameters (invalid name and/or type) recognised"


class APIError(Exception):
    pass


class ZilliqaAPI:
    """Json-RPC interface of Zilliqa APIs."""
    class APIMethod:
        def __init__(self, api: "ZilliqaAPI", method_name: str):
            self.api = api
            self.method_name = method_name

        def __call__(self, *params, **kwargs):
            return self.api.call(self.method_name, *params, **kwargs)

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def __getattr__(self, item: str):
        return ZilliqaAPI.APIMethod(self, method_name=item)

    def call(self, method_name: str, *params, **kwargs):
        response = requests.post(
                self.endpoint, json=request(method=method_name, params=params)
            )
        parsed = parse(response.json())
        if isinstance(parsed, Ok):
            return parsed.result
        else:
            print(parsed.message)
            raise APIError(parsed.message)

if "__main__" == __name__:
    _api = ZilliqaAPI("https://dev-api.zilliqa.com/")
    print(_api.GetCurrentMiniEpoch())
    print(_api.GetCurrentDSEpoch())
    print(_api.GetBalance("b50c2404e699fd985f71b2c3f032059f13d6543b"))
    print(_api.GetBalance("4BAF5faDA8e5Db92C3d3242618c5B47133AE003C"))
    print(_api.GetBalance("4BAF5faDA8e5Db92C3d3242618c5B47133AE003C"))

