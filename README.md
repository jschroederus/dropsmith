# Dropsmith

**A product forge, not an image generator.** Plenty of tools make an image from a
prompt. Dropsmith makes a *listable product*: one command turns a niche into a
premium, text-baked design **and** the marketplace listing to sell it — title,
description, 13 search tags, suggested price. Bring your own Gemini key.

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

## As an OpenClaw skill

Dropsmith ships as an [OpenClaw](https://github.com/openclaw/openclaw) skill in
[`skill/`](skill/) — drop it in your workspace and the agent can forge product
drops on request:

```bash
cp -r skill ~/.openclaw/workspace/skills/dropsmith
chmod +x ~/.openclaw/workspace/skills/dropsmith/scripts/dropsmith
# then, in OpenClaw: "make me a drop for a mid-century palm springs gallery wall"
```

The skill calls `scripts/dropsmith`, which runs the tool in an isolated `uv` env
(nothing installed globally) and needs `GEMINI_API_KEY` set. It's positioned as a
product forge — the listing-and-design vertical the raw Gemini CLI doesn't cover.
See [`skill/SKILL.md`](skill/SKILL.md).

## The story

[**The prompt was the disease**](docs/the-prompt-was-the-disease.md) — why the
guardrails in your image prompt are probably scar tissue making output worse, and
the `google-genai` async bug that silently eats your calls.

## Examples

Sample listings live in [`examples/`](examples/); regenerate the designs with your
own key via [`examples/generate.sh`](examples/generate.sh).

## License

MIT. See [LICENSE](LICENSE). Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
