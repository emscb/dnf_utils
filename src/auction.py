import dataclasses
from urllib.parse import urlencode, quote

import requests
from env_var import API_KEY


@dataclasses.dataclass
class AuctionRegisteredItem:
    auction_no: int
    item_id: str
    item_name: str
    item_type_detail: str
    count: int
    price: int


def search_by_item_name(item_name: str, *, limit: int = 100) -> list[AuctionRegisteredItem]:
    response = requests.get("https://api.neople.co.kr/df/auction?" + urlencode(
        {
            "apikey": API_KEY,
            "limit": limit,
            "sort": "unitPrice:asc",
            "itemName": item_name,
            "wordType": "front",
        }, quote_via=quote,
    ))
    if response.status_code != 200:
        print("검색 실패")
        print(response.text)
        return []

    rsp = response.json()
    registered_items = list()
    for row in rsp.get("rows", []):
        registered_items.append(AuctionRegisteredItem(
            auction_no=row["auctionNo"],
            item_id=row["itemId"],
            item_name=row["itemName"],
            item_type_detail=row["itemTypeDetail"],
            count=row["count"],
            price=row["unitPrice"],
        ))

    return registered_items
