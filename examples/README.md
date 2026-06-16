# Examples

Every file here is **real, unedited dropsmith output** — the `.png` design and the
`.json` listing exactly as the model returned them, no touch-ups. Each pair came
from a single niche string:

| Niche | Design | Listing |
|-------|--------|---------|
| `mid-century palm springs gallery wall` | [png](mid-century-palm-springs-gallery-wall.png) | [json](mid-century-palm-springs-gallery-wall.json) |
| `vintage americana block party invitation` | [png](vintage-americana-block-party-invitation.png) | [json](vintage-americana-block-party-invitation.json) |
| `letterpress coffee roaster brand kit` | [png](letterpress-coffee-roaster-brand-kit.png) | [json](letterpress-coffee-roaster-brand-kit.json) |
| `coastal big sur travel poster` | [png](coastal-big-sur-travel-poster.png) | [json](coastal-big-sur-travel-poster.json) |

Note what the model *invented*: the block-party invite has a host family, a date,
and an RSVP; the coffee kit has a tagline and an "est. 2023." None of that was in
the niche — the niche is creative direction, and dropsmith lets the model write the
finished copy.

## Regenerate

Each run is non-deterministic — that's the point; the model is designing, not
stamping a template. Make your own:

```bash
export GEMINI_API_KEY=...        # https://aistudio.google.com/apikey
./generate.sh                    # writes fresh drops to ./out/
```
