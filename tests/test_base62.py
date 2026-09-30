import pytest

from app.urls.base62 import (
    BASE62_ALPHABET,
    SHORT_CODE_LENGTH,
    decode_base62,
    encode_base62,
    generate_base62_code,
)


@pytest.mark.parametrize(
    ("number", "encoded"),
    [
        (0, "0"),
        (1, "1"),
        (61, "Z"),
        (62, "10"),
        (11157, "2TX"),
    ],
)
def test_encode_base62(number: int, encoded: str) -> None:
    assert encode_base62(number) == encoded


@pytest.mark.parametrize(
    "number",
    [
        0,
        1,
        61,
        62,
        11157,
        1_000_000,
        365_000_000_000,
    ],
)
def test_base62_round_trip(number: int) -> None:
    encoded = encode_base62(number)
    assert decode_base62(encoded) == number


def test_generate_base62_code() -> None:
    short_code = generate_base62_code()

    assert len(short_code) == SHORT_CODE_LENGTH
    assert set(short_code) <= set(BASE62_ALPHABET)