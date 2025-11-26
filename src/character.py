from __future__ import annotations

from dataclasses import dataclass
from typing import NotRequired, TypedDict
from urllib.parse import urlencode, quote

import requests

from env_var import API_KEY


class APICharacter(TypedDict):
    serverId: str
    characterId: str
    characterName: str
    level: int
    jobId: str
    jobGrowId: str
    jobName: str
    jobGrowName: str
    fame: NotRequired[int]  # 명성


@dataclass
class Character:
    server_id: str
    character_id: str
    character_name: str
    level: int
    job_grow_name: str
    fame: int | None

    @staticmethod
    def from_api(row: APICharacter) -> Character:
        try:
            return Character(
                server_id=row["serverId"],
                character_id=row["characterId"],
                character_name=row["characterName"],
                level=row["level"],
                job_grow_name=row["jobGrowName"],
                fame=row.get("fame"),
            )
        except KeyError as e:
            print(f"캐릭터 검색 결과 파싱 실패: KeyError: {e}")
            raise

    @staticmethod
    def from_apis(rows: list[APICharacter]) -> list[Character]:
        return [Character.from_api(row) for row in rows]


def get_character_list(name: str, server_id: str | None = "all") -> list[Character]:
    if not (2 <= len(name) <= 12):
        print("캐릭터 이름으로 검색은 최소 2자에서 최대 12자까지 입력해야 함")
        return []

    response = requests.get(f"https://api.neople.co.kr/df/servers/{server_id}/characters?" + urlencode(
        {
            "apikey": API_KEY,
            "characterName": name,
            "wordType": "full",
            "limit": 100,
        }, quote_via=quote,
    ))
    if response.status_code != 200:
        print("검색 실패")
        print(response.text)
        return []

    rsp = response.json()
    return Character.from_apis(rsp.get("rows", []))


def get_set_info(character: Character) -> (str, str, int):
    response = requests.get(f"https://api.neople.co.kr/df"
                            f"/servers/{character.server_id}"
                            f"/characters/{character.character_id}/equip/equipment"
                            f"?apikey={API_KEY}")
    if response.status_code != 200:
        print("검색 실패")
        print(response.text)
        response.raise_for_status()

    rsp = response.json()
    if (set_item_info := rsp.get("setItemInfo", [])) is None or len(set_item_info) == 0:
        raise Exception("세트 아이템 정보 없음")

    try:
        set_id = set_item_info[0]["setItemId"]
        set_name = set_item_info[0]["setItemName"]
        set_rarity_name = set_item_info[0]["setItemRarityName"]
    except (IndexError, KeyError):
        raise Exception("세트 아이템 정보 없음")

    whole_set_point = 0
    for equipment in rsp.get("equipment", []):
        for tune in equipment.get("tune", []):
            if (set_point := tune.get("setPoint")) is not None and isinstance(set_point, int):
                whole_set_point += set_point
        upgrade_info = equipment.get("upgradeInfo", {})
        if upgrade_info.get("setItemId") == set_id and (
                set_point := upgrade_info.get("setPoint")) is not None and isinstance(set_point, int):
            whole_set_point += set_point

    return set_name, set_rarity_name, whole_set_point
