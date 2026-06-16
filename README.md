# Dropsmith

**Turn a niche into a listable digital product.** One command: a premium,
text-baked design and ready-to-paste marketplace listing (title, description,
tags, price). Bring your own Gemini key.

```bash
dropsmith "mid-century palm springs gallery wall"
```

```
out/
  mid-century-palm-springs-gallery-wall.png    # premium design, legible baked text
  mid-century-palm-springs-gallery-wall.json   # { title, description, tags, suggested_price_usd }
```

## Why

Most "AI product" tools fight the model: zero-text rules, forbidden-motif walls,
hardcoded palettes — scaffolding built for weak models that makes modern ones
produce gibberish and AI-slop. Dropsmith does the opposite: it briefs the model
like a creative director briefs a great designer (product, theme, palette, mood,
the real copy, "render it legibly"). The result reads designer-made, not
generated. See [`dropsmith/prompts.py`](dropsmith/prompts.py).

## Install

```bash
pip install dropsmith         # or: pipx install dropsmith
cp .env.example .env          # add your GEMINI_API_KEY
```

Get a key at https://aistudio.google.com/apikey.

## Usage

```bash
dropsmith "vintage americana block party invitation"
dropsmith "coastal travel poster" --copy "Visit Big Sur"   # bake exact hero text
dropsmith "letterpress coffee roaster brand kit" -o ./drops
```

Or as a library:

```python
import asyncio
from dropsmith import generate_drop

drop = asyncio.run(generate_drop("heritage screenprint gig poster"))
print(drop.listing["title"])
open("design.png", "wb").write(drop.image_bytes)
```

## The aiohttp gotcha (why this works when your code doesn't)

`google-genai` 2.8.x ships an aiohttp-based async transport that raises a bare
`AssertionError` (`assert self._connector is not None`) on **every** `.aio`
call against current aiohttp — and it's swallowed by typical `try/except`, so
your feature just silently returns nothing. Dropsmith forces the httpx
transport instead:

```python
genai.Client(
    api_key=key,
    http_options=types.HttpOptions(async_client_args={"transport": httpx.AsyncHTTPTransport()}),
)
```

This flips the SDK's internal `_use_aiohttp()` off. If your Gemini async calls
mysteriously do nothing, this is almost certainly why.

## Models

Configurable via env (defaults shown):

```
DROPSMITH_IMAGE_MODEL=gemini-3-pro-image-preview
DROPSMITH_TEXT_MODEL=gemini-3.1-pro-preview
```

## License

MIT. See [LICENSE](LICENSE). Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
