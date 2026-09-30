from secrets import randbelow

BASE62_ALPHABET = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)

BASE = len(BASE62_ALPHABET)
SHORT_CODE_LENGTH = 12

CHARACTER_VALUES = { character: index for index, character in enumerate(BASE62_ALPHABET)}

def encode_base62(value: int, min_length: int = 1) -> str:
    if value < 0:
        raise ValueError('Base62 cannot encode a negative number')

    if value == 0:
        encoded = BASE62_ALPHABET[0]
    else:
        characters: list[str] = []

        while value:
            value, remainder = divmod(value, BASE)
            characters.append(BASE62_ALPHABET[remainder])

        encoded = ''.join(reversed(characters))

    return encoded.rjust(min_length, BASE62_ALPHABET[0])

def decode_base62(value: str) -> int:
    if not value:
        raise ValueError('Base62 value cannot be empty')

    result = 0
    for character in value:
        try:
            character_value = CHARACTER_VALUES[character]
        except KeyError as e:
            raise ValueError(f'Invalid Base62 character: {character!r}') from e

        result = result * BASE + character_value

    return result

def generate_base62_code(length: int = SHORT_CODE_LENGTH) -> str:
    if length < 1:
        raise ValueError('Short code length must be positive')

    random_value = randbelow(BASE**length)

    return encode_base62(random_value, min_length=length)