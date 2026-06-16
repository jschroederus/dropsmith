"""Prompt builders for Dropsmith.

The design brief here is the distilled, battle-tested version: brief the model
like a creative director briefs an excellent designer (product, theme, palette,
mood, the real copy, "render it legibly"). The opposite approach — stacking
"zero text" rules, forbidden-motif walls, and hardcoded palettes — was built
for weaker models and actively produces gibberish and AI-slop on modern ones.
Keep this lean.
"""

from __future__ import annotations

_DESIGN_BRIEF = """A premium, photorealistic {product} for the "{niche}" theme. {width}x{height}px, {orientation}.

Palette: {palette}.
Design direction: {style}; overall mood {mood}. Confident composition with strong
visual hierarchy, generous whitespace, fine detail, and a premium paper / material
texture. It must read as designer-made at thumbnail size, with a clear point of view
a real buyer would pay for.
{copy_block}
Render ALL text crisp, perfectly legible, correctly spelled, and integrated as
finished professional typography — never placeholder bars, squiggles, or fake
lettering. The theme must come from the niche itself. Add at most one small tasteful
emblem only if it genuinely fits. Avoid clutter, stacked badges or heraldry, garish
colors, generic stock motifs, and childish cues."""


def build_design_prompt(
    niche: str,
    *,
    product: str = "poster / wall-art print",
    width: int = 1024,
    height: int = 1024,
    style: str = "refined modern editorial",
    mood: str = "premium and confident",
    palette: str = "let the niche dictate a cohesive, tasteful palette",
    copy: str | None = None,
) -> str:
    """Assemble a clean creative brief for the image model.

    Key behavior: the niche is creative DIRECTION, not text to print. Without
    explicit ``copy``, the model is told to INVENT believable, realistic finished
    copy appropriate to the product (a party invite gets a plausible host/date/
    venue; a poster gets a real-feeling headline) — never to print this brief
    verbatim. Pass ``copy`` only when you want exact words baked in.
    """
    if copy:
        copy_block = f'Render this EXACT copy as the hero text, spelled correctly: "{copy}".\n'
    else:
        copy_block = (
            f'The phrase "{niche}" is creative DIRECTION — the brief, never the text. Invent the '
            "finished copy a real designer would actually set: specific, evocative, with a point of "
            "view. A travel poster names the place or a real local phrase; an invitation gets a "
            "plausible host, date, and venue; a brand kit gets an actual brand name and tagline. "
            "Do NOT headline the piece with words that describe its own style, genre, medium, era, "
            'or mood (never "Desert Modernist", "Mid-Century", "Vintage", "Retro", "Letterpress", '
            '"Coastal" as the title), and avoid limp filler adjectives (majestic, premium, stunning, '
            "elegant, timeless, beautiful). Write what belongs on the product — not a label of what it is.\n"
        )
    return _DESIGN_BRIEF.format(
        product=product,
        niche=niche,
        width=width,
        height=height,
        orientation="portrait" if height >= width else "landscape",
        palette=palette,
        style=style,
        mood=mood,
        copy_block=copy_block,
    )


LISTING_SYSTEM = (
    "You are an expert Etsy/marketplace listing copywriter for premium digital "
    "products. Write copy that is specific, tasteful, and conversion-focused — "
    "no keyword soup, no generic filler."
)


def build_listing_prompt(niche: str) -> str:
    return (
        f'Write a marketplace listing for a premium digital product in the niche: "{niche}".\n'
        "Return STRICT JSON with keys:\n"
        '  "title": catchy, specific, <= 140 chars\n'
        '  "description": 2-3 short paragraphs selling the dream + what is included\n'
        '  "tags": array of 13 lowercase search tags, each <= 20 chars\n'
        '  "suggested_price_usd": a realistic number (digital download, 3-25)\n'
        "Return ONLY the JSON object, no prose."
    )
