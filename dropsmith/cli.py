"""Dropsmith CLI: turn a niche into a listable digital product."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

from .generator import generate_drop


def _load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE lines from a local .env, without overriding the
    real environment. Stdlib-only — no python-dotenv dependency. Keeps the key
    in a gitignored file instead of the shell history."""
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "drop"


async def _run(niche: str, out_dir: Path, copy: str | None) -> int:
    print(f"forging drop for: {niche!r} ...", file=sys.stderr)
    drop = await generate_drop(niche, copy=copy)

    out_dir.mkdir(parents=True, exist_ok=True)
    slug = _slug(niche)
    img_path = out_dir / f"{slug}.png"
    json_path = out_dir / f"{slug}.json"
    img_path.write_bytes(drop.image_bytes)
    json_path.write_text(json.dumps(drop.listing, indent=2))

    print(f"\n  design   -> {img_path}  ({len(drop.image_bytes):,} bytes)")
    print(f"  listing  -> {json_path}")
    title = drop.listing.get("title", "")
    price = drop.listing.get("suggested_price_usd", "?")
    print(f"\n  {title}")
    print(f"  suggested ${price}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dropsmith",
        description="Turn a niche into a listable digital product: premium design + marketplace listing.",
    )
    parser.add_argument("niche", help='e.g. "mid-century palm springs gallery wall"')
    parser.add_argument("-o", "--out", default="out", help="output directory (default: ./out)")
    parser.add_argument("--copy", default=None, help="exact hero text to bake into the design")
    args = parser.parse_args(argv)
    _load_dotenv()

    try:
        return asyncio.run(_run(args.niche, Path(args.out), args.copy))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
