#!/usr/bin/env bash
# Regenerate every sample drop. Needs GEMINI_API_KEY in the environment.
set -euo pipefail
cd "$(dirname "$0")/.."

niches=(
  "mid-century palm springs gallery wall"
  "vintage americana block party invitation"
  "letterpress coffee roaster brand kit"
  "coastal big sur travel poster"
)

for n in "${niches[@]}"; do
  echo ">> $n"
  python -m dropsmith.cli "$n" -o examples/out
done

echo "done -> examples/out/"
