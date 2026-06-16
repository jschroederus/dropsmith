# Contributing

PRs welcome. Keep it small and focused.

- `pip install -e ".[dev]"` (or just `pip install -e .`)
- Code style: ruff. Run `ruff check .` before pushing.
- The design philosophy is "brief the model like a creative director" — keep
  prompts lean. Don't add forbidden-motif walls or zero-text rules; they hurt
  modern models. See `dropsmith/prompts.py`.
