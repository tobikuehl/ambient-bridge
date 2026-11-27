#!/usr/bin/env bash
set -e

HOST="${1:-https://localhost}"

echo "Sending simulated AI documentation draft to $HOST ..."

curl -k -s -X POST "$HOST/api/drafts" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "local-ambient-scribe (whisper-large-v3 + local-llm)",
    "title": "Progress Note Draft (Demo Session)",
    "content": "▶ PART: ⚡5/10 (SIJ-L) | ⬇Walking | ↗Sitting | ⭆ R. Thigh | ☼Morning\n\n### Subjective & Objective (LIFO)\n- Client reports noticeable relaxation in cervical/thoracic region since last session.\n- Manual mobilization performed; home exercise plan reviewed (follow-up in 14 days)."
  }' | python3 -m json.tool

echo ""
echo "Done! Open $HOST in your browser (or tablet PWA) to review and copy the draft."
