# X launch thread — dropsmith

Goal: ship the OSS + earn engagement from the agent/Gemini crowd. Angle = a named
prompt philosophy that anyone doing AI image gen can use today. NOT "here's another
image tool" — lead with the insight, the tool is just proof.

Honest framing note: the `google-genai` aiohttp bug is a **Python SDK** bug. It
does NOT affect the OpenClaw Gemini skill (that's the `gemini` CLI) or OpenClaw's
TS core. So this thread does NOT claim it fixes anyone's skill — it's a general PSA
for people calling google-genai from Python. Keep it that way.

Post the design PNG from your first good generation as the media on tweet 1.

---

**1/ (hook + media)**
I spent weeks blaming the model for AI-slop output. It was my prompt the whole time.

Open-sourced dropsmith: a niche string → a finished, sellable design + its
marketplace listing. One command. Built on Gemini 3 Pro Image.

The two things I learned ↓

🔗 github.com/jschroederus/dropsmith

**2/**
My image prompt had grown into a 6-layer guardrail wall: a "render zero text"
rule, ~30 forbidden motifs, hardcoded palettes, an anti-slop block, a taste gate.

Every layer was scar tissue from a past failure on a weaker model.

Output kept getting *worse*.

**3/**
The fix was subtraction. I deleted all of it and wrote ONE creative brief — the
way you'd brief a good designer. Product, theme, palette, mood, the real copy,
"render it legibly." Stop.

First generation off the clean brief: premium, perfectly legible. The model could
do it the whole time.

**4/**
The lesson: guardrails are scar tissue with no expiry date. When the model gets
better, your old "don't do X" rules don't go neutral — they go actively harmful.

Re-run your prompt naked now and then. Delete what the model has outgrown.

**5/ (Python PSA — for anyone calling google-genai directly)**
If you call `google-genai` from Python async: 2.8.x's aiohttp transport raises a
bare `assert self._connector is not None` on every `.aio` call. It's swallowed by
normal try/except — your async Gemini call just silently returns nothing.

Force the httpx transport:

```python
genai.Client(api_key=key, http_options=types.HttpOptions(
    async_client_args={"transport": httpx.AsyncHTTPTransport()}))
```

**6/**
dropsmith isn't an image tool — `gemini -p` already makes images. It's a *product
forge*: niche in, finished design + marketplace listing (title, copy, 13 tags,
price) out. The vertical, not the pixels.

Full writeup: github.com/jschroederus/dropsmith/blob/main/docs/the-prompt-was-the-disease.md

MIT. Take what's useful.

---

## LOCKED — OpenClaw-origin reply thread (post this one)

Reply to his OpenClaw beta + Gemini Flash 3.1 post:
https://x.com/steipete/status/2030508141419372667

**1/**
> Funny timing. After first trying OpenClaw in February, I had a fully working
> generator for Geniche within 72 hours — a taste-driven product builder: agent
> researches trending items, generates fully-editable designs, auto-lists them to
> a marketplace. Pushing Gemini 3 Pro Image for it taught me something ↓

**2/ (attach the PALM SPRINGS poster: examples/mid-century-palm-springs-gallery-wall.png)**
> The output looked like AI slop. Spent weeks blaming the model. It was my prompt —
> a wall of guardrails (zero-text rules, forbidden motifs, locked palettes), all
> scar tissue from a weaker model, all making it *worse*. Deleted every layer,
> briefed it like a designer. Then this ↓

**3/**
> Carved the prompt engine into a tiny MIT tool — niche string → finished design +
> marketplace listing, one command. github.com/jschroederus/dropsmith

---

## Reply-to-steipete drafts (philosophy, on its own merit — not a tag-beg)

Post as a reply to one of his Gemini / AI-image posts. Media = the Desert Modernist
Palm Springs poster (examples/mid-century-palm-springs-gallery-wall.png).

**A — single reply (recommended):**
> Spent weeks blaming the model for AI-slop output. It was my prompt.
>
> I'd stacked guardrails — "render zero text," forbidden motifs, locked palettes —
> all scar tissue from a weaker model. Deleted every layer, wrote one
> creative-director brief instead. First gen: this. ↓
>
> The model had it the whole time.

**B — two-tweet, includes the link:**
> 1/ Spent weeks blaming the model for slop. It was my prompt. I'd built a 6-layer
> guardrail wall — zero-text rules, forbidden motifs, hardcoded palettes — scar
> tissue from a weaker model. Output kept getting *worse*.
>
> 2/ Deleted all of it. One creative-director brief — product, palette, mood,
> "render it legibly." First gen off the clean prompt ↓ [image]. Open-sourced the
> whole thing: github.com/jschroederus/dropsmith

**C — sharpest / most quotable:**
> Your image prompt's guardrails are probably scar tissue.
>
> Every "don't render text / no badges / use these colors" rule was written for a
> weaker model. On a current one they don't go neutral — they make output *worse*.
> I deleted all of mine and the model finally did this ↓

## Notes
- Do NOT @ steipete with a "fixes your skill" claim — his Gemini skill is the
  `gemini` CLI and never touches the Python aiohttp bug. That claim is false; using
  it would torch credibility with exactly the audience you want.
- Better path to that crowd: reply to a Gemini/AI-image post of his with tweet 3+4
  (the anti-scaffolding philosophy) on its own merit. An idea worth resharing beats
  a tagged launch.
- Tweet 5 is a genuine PSA for the Python google-genai users — true and useful, just
  don't attach it to anyone's specific project.
- Single-tweet alternative (if the thread feels long):
  > Open-sourced dropsmith: niche string → finished sellable design + marketplace
  > listing, one command, on Gemini 3 Pro Image. The lesson inside: your image
  > prompt's guardrails are probably scar tissue making output *worse* on modern
  > models. Delete them. MIT. [link]
```
