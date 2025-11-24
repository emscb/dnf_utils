from __future__ import annotations

from typing import TypedDict
from urllib.parse import urlencode, quote

import requests

from env_var import API_KEY


class APIServer(TypedDict):
    serverId: str
    serverName: str


def get_server_list() -> list[APIServer]:
    response = requests.get("https://api.neople.co.kr/df/servers?" + urlencode(
        {
            "apikey": API_KEY,
        }, quote_via=quote,
    ))
    if response.status_code != 200:
        print("검색 실패")
        print(response.text)
        return []

    rsp = response.json()
    return rsp.get("rows", [])
