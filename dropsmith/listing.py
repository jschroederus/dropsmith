"""Parse and validate a marketplace listing out of a model response.

Stdlib-only on purpose: no SDK imports here, so the parsing contract is unit
testable without a Gemini key or network.
"""

from __future__ import annotations

import json
import re

REQUIRED_LISTING_KEYS = ("title", "description", "tags", "suggested_price_usd")
_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


def parse_listing(raw: str) -> dict:
    """Pull a valid listing object out of a model response.

    Models wander: code fences, a sentence before the JSON, a trailing note.
    Strip fences, grab the first balanced ``{...}`` block, then validate that
    every required key is present and well-typed. Raises ``ValueError`` on any
    failure so the caller can retry rather than ship a broken listing.
    """
    text = (raw or "").strip()
    fenced = _FENCE.search(text)
    if fenced:
        text = fenced.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found in listing response")
    data = json.loads(text[start : end + 1])

    missing = [k for k in REQUIRED_LISTING_KEYS if k not in data]
    if missing:
        raise ValueError(f"listing missing keys: {missing}")
    if not isinstance(data["tags"], list) or not data["tags"]:
        raise ValueError("listing 'tags' must be a non-empty list")
    try:
        data["suggested_price_usd"] = float(data["suggested_price_usd"])
    except (TypeError, ValueError) as exc:
        raise ValueError("listing 'suggested_price_usd' is not a number") from exc
    return data
