from src.character import get_character_list, get_set_info


def replace_space_to_em_space(text: str, rfill: int | None = None) -> str:
    if rfill is None:
        return text.replace(" ", "\u2003")

    return text.replace(" ", "\u2003") + (rfill - len(text)) * "\u2003"


if __name__ == '__main__':
    characters = get_character_list("용든츄")
    characters = [c for c in characters if c.fame is not None]
    characters = sorted(characters, key=lambda c: c.fame, reverse=True)
    for character in characters:
        msg = f"{character.character_name:5s}   {replace_space_to_em_space(character.job_grow_name, 10)} | "

        try:
            set_name, set_rarity_name, set_point = get_set_info(character)
            msg += f"{replace_space_to_em_space(set_name, 18)} | {set_rarity_name}"
            if set_point <= 2550:
                msg += f"({set_point})"
            else:
                extra_70_count = (set_point - 2550) // 70
                extra_mod_70 = (set_point - 2550) % 70
                msg += f"({'2550' + '+70' * extra_70_count + ('' if extra_mod_70 == 0 else '+' + str(extra_mod_70))})"
        except Exception as e:
            msg += f"세트 정보 오류 ({e})"

        print(msg)
