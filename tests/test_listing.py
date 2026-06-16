"""Tests for the listing parser — stdlib only, no Gemini key or network needed."""

import pytest

from dropsmith.listing import parse_listing

_GOOD = '{"title":"x","description":"y","tags":["a","b"],"suggested_price_usd":12}'


def test_plain_json():
    out = parse_listing(_GOOD)
    assert out["title"] == "x"
    assert out["tags"] == ["a", "b"]
    assert out["suggested_price_usd"] == 12.0
    assert isinstance(out["suggested_price_usd"], float)


def test_code_fenced():
    assert parse_listing(f"```json\n{_GOOD}\n```")["title"] == "x"


def test_prose_wrapped():
    raw = f"Here is your listing:\n{_GOOD}\nHope that helps!"
    assert parse_listing(raw)["title"] == "x"


def test_price_as_string_is_coerced():
    raw = _GOOD.replace("12", '"9"')
    assert parse_listing(raw)["suggested_price_usd"] == 9.0


@pytest.mark.parametrize(
    "raw",
    [
        "no json here at all",
        '{"title":"x"}',  # missing keys
        '{"title":"x","description":"y","tags":[],"suggested_price_usd":1}',  # empty tags
        '{"title":"x","description":"y","tags":["a"],"suggested_price_usd":"free"}',  # bad price
    ],
)
def test_invalid_raises(raw):
    with pytest.raises(ValueError):
        parse_listing(raw)
