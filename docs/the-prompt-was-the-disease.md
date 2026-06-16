# The prompt was the disease

I spent weeks blaming the model for garbage output. It was the prompt the whole
time. This is the short version of what I learned building [dropsmith](https://github.com/jschroederus/dropsmith) —
a tool that turns a niche string into a finished, sellable design and the
marketplace listing to go with it — plus one genuinely nasty bug in `google-genai`
that will silently eat your async calls.

## Part 1: stop building guardrails for a model that outgrew them

My image generations looked like AI slop: gibberish text, stacked fake badges,
muddy heraldry, the lot. So I did what everyone does — I added rules. Then more
rules. The design prompt grew into a six-layer wall:

- a hard **"render zero text"** rule (because the old model spelled like a drunk)
- a list of **~30 forbidden motifs** (no crests, no banners, no ribbons…)
- **hardcoded palettes** ("use Mother's Day pinks")
- a separate **anti-slop style block**
- per-niche art-direction overrides
- a taste gate that scored pixels and rejected anything "too busy"

Every layer was a scar from a past failure on a weaker model. And the output got
*worse*. The zero-text rule produced blank poster-shaped rectangles. The
forbidden-motif list made the model nervous and generic. The hardcoded palettes
fought the actual niche.

The fix was subtraction. I deleted all of it and wrote one creative brief — the
way you'd brief a good designer:

> A premium {product} for the "{niche}" theme. Palette: {let the niche decide}.
> Strong visual hierarchy, generous whitespace, premium material texture. Render
> all text crisp, legible, correctly spelled, integrated as finished typography.
> The theme comes from the niche itself.

That's it. The first real generation off the clean brief was a premium, perfectly
legible product. The model had been able to do this the whole time — the
scaffolding was holding it back, not propping it up.

**The lesson:** guardrails are scar tissue. They're made-up scaffolding for a
specific past failure, and they don't expire on their own. When the model gets
better, the guardrails don't get *neutral* — they get *actively harmful*, because
you're now constraining a capable model with rules written for an incapable one.
Treat every "don't do X" in a prompt as a liability with a maturity date. Re-run
the naked version periodically. Delete what the model has outgrown.

Two corollaries that fell out of this:

1. **The niche is direction, not text.** Don't print the brief on the canvas.
   Tell the model the phrase is creative direction and let it *invent* believable
   finished copy — a party invite gets a plausible host and date, a poster gets a
   real headline. Prompt-echo is the tell that screams "generated."
2. **A pixel-stats taste gate cannot judge taste.** It rejected good designs for
   being "busy" and passed bland ones for being calm. It's now advisory at most.

## Part 2: the `google-genai` aiohttp bug that returns nothing

While rebuilding this, every async Gemini call started silently returning nothing.
No exception I could see, no image, no error — the feature just produced empty
output and moved on.

`google-genai` 2.8.x ships an aiohttp-based async transport. Against current
aiohttp, every `.aio` call hits this:

```
assert self._connector is not None
```

A bare `AssertionError`, raised deep in the SDK's async path. And because it's a
bare assertion inside an `async` call, a normal `try/except Exception` around your
feature swallows it and you never see a traceback — your code looks like it
"worked" and returned empty.

The fix is to never let the SDK touch its aiohttp path. Force the httpx transport:

```python
from google import genai
from google.genai import types
import httpx

genai.Client(
    api_key=key,
    http_options=types.HttpOptions(
        async_client_args={"transport": httpx.AsyncHTTPTransport()}
    ),
)
```

Passing `async_client_args` flips the SDK's internal `_use_aiohttp()` off and
routes async through the working httpx client. If your Gemini async calls
mysteriously do nothing — this is almost certainly why. It cost me a day; it
should cost you about thirty seconds.

## Takeaways

- Periodically run your prompt **naked**. The model may have outgrown its leash.
- Guardrails are dated scar tissue — review and delete, don't accumulate.
- Make the model invent copy; never print the brief.
- On `google-genai` 2.8.x, force httpx or your async calls die silently.

Both lessons are baked into dropsmith — the clean brief lives in
[`dropsmith/prompts.py`](../dropsmith/prompts.py), the transport fix in
[`dropsmith/generator.py`](../dropsmith/generator.py). MIT licensed; take what's
useful.
