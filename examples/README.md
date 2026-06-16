# Examples

The `*.json` files here are real-shaped sample **listings** — exactly what
`dropsmith` writes next to each design. They're committed so you can see the
output contract without a key.

The matching `*.png` designs are **not** committed (a design tool that ships
canned images is lying about what it does). Generate them yourself — one command,
your key, ~10 seconds each:

```bash
export GEMINI_API_KEY=...        # https://aistudio.google.com/apikey
./generate.sh                    # regenerates every sample niche into ./out/
```

Then drop a few of the resulting PNGs back into this folder if you want a gallery
in the README. Each run is non-deterministic — that's the point; the model is
designing, not stamping a template.
