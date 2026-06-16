---
name: dropsmith
description: "Forge a listable digital product from a niche: one premium text-baked design (PNG) plus its marketplace listing (title, description, 13 tags, price). A product forge, not a general image tool."
homepage: https://github.com/jschroederus/dropsmith
metadata:
  {
    "openclaw":
      {
        "emoji": "🛠️",
        "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Dropsmith

Use when the user wants a **sellable digital product**, not just an image: Etsy /
print-on-demand art, a gallery-wall print, a poster, a party invitation, a brand
kit — *plus* the marketplace copy to list it. The user gives a niche; dropsmith
returns one finished design and its listing JSON in a single shot.

This is the vertical the raw Gemini CLI doesn't cover: `gemini -p` makes an image;
dropsmith makes a *product* — design + title + description + 13 search tags + a
suggested price, briefed so the design reads designer-made and the copy is
conversion-focused.

API key (required)

- `GEMINI_API_KEY` — get one at https://aistudio.google.com/apikey

Quick start

```bash
{baseDir}/scripts/dropsmith "mid-century palm springs gallery wall"
```

Bake exact hero text instead of letting the model invent copy:

```bash
{baseDir}/scripts/dropsmith "coastal travel poster" --copy "Visit Big Sur"
```

Choose an output directory (default `./out`):

```bash
{baseDir}/scripts/dropsmith "letterpress coffee roaster brand kit" -o ./drops
```

Output

```
out/
  <slug>.png    # premium design, legible baked text
  <slug>.json   # { title, description, tags, suggested_price_usd }
```

The script runs dropsmith in an isolated `uv` env on first call — nothing is
installed globally.

## How it briefs the model

The niche is creative *direction*, not text to print. Without `--copy`, the model
invents believable finished copy (a party invite gets a plausible host, date, and
venue; a poster gets a real headline) rather than printing the brief verbatim.
Dropsmith briefs like a creative director — product, theme, palette, mood, "render
it legibly" — and deliberately avoids the zero-text rules, forbidden-motif walls,
and hardcoded palettes that make modern models produce AI-slop. See the writeup:
https://github.com/jschroederus/dropsmith/blob/main/docs/the-prompt-was-the-disease.md
