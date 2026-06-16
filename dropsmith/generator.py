"""Core generation: niche -> design image + listing copy, via Gemini.

Includes the httpx-transport workaround for the google-genai aiohttp bug
(``assert self._connector is not None`` on every ``.aio`` call in 2.8.x). A
custom transport flips the SDK's ``_use_aiohttp()`` off and routes async
through the working httpx client. See README "The aiohttp gotcha".
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass

import httpx
from google import genai
from google.genai import types

from .listing import parse_listing
from .prompts import LISTING_SYSTEM, build_design_prompt, build_listing_prompt

DEFAULT_IMAGE_MODEL = os.getenv("DROPSMITH_IMAGE_MODEL", "gemini-3-pro-image-preview")
DEFAULT_TEXT_MODEL = os.getenv("DROPSMITH_TEXT_MODEL", "gemini-3.1-pro-preview")


def _client() -> genai.Client:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env and add your key.")
    # The fix: force the httpx async transport so google-genai never touches its
    # broken aiohttp path. A fresh client per call keeps no event-loop-bound state.
    return genai.Client(
        api_key=key,
        http_options=types.HttpOptions(async_client_args={"transport": httpx.AsyncHTTPTransport()}),
    )


@dataclass
class Drop:
    niche: str
    image_bytes: bytes
    listing: dict


def _extract_image(response) -> bytes:
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            inline = getattr(part, "inline_data", None)
            data = getattr(inline, "data", None)
            if data:
                return base64.b64decode(data) if isinstance(data, str) else data
    raise RuntimeError("Image generation returned no image data")


async def generate_design(niche: str, *, copy: str | None = None) -> bytes:
    client = _client()
    prompt = build_design_prompt(niche, copy=copy)
    resp = await client.aio.models.generate_content(
        model=DEFAULT_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"], temperature=0.6),
    )
    return _extract_image(resp)


async def generate_listing(niche: str) -> dict:
    client = _client()
    contents = f"{LISTING_SYSTEM}\n\n{build_listing_prompt(niche)}"
    last_error: Exception | None = None
    # One retry: the model occasionally wraps prose around the JSON or drops a
    # key. A second pass with a blunt reminder almost always lands it.
    for attempt in range(2):
        prompt = contents if attempt == 0 else f"{contents}\n\nReturn ONLY the JSON object. No prose, no code fence."
        resp = await client.aio.models.generate_content(
            model=DEFAULT_TEXT_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7, max_output_tokens=2048),
        )
        try:
            return parse_listing(getattr(resp, "text", "") or "")
        except (ValueError, json.JSONDecodeError) as exc:
            last_error = exc
    raise RuntimeError(f"Could not parse a valid listing from the model: {last_error}")


async def generate_drop(niche: str, *, copy: str | None = None) -> Drop:
    """Generate a full product drop: design image + listing copy."""
    image_bytes = await generate_design(niche, copy=copy)
    listing = await generate_listing(niche)
    return Drop(niche=niche, image_bytes=image_bytes, listing=listing)
