#!/usr/bin/env bash
# Theme toggler and switcher for Hisense SmartTV 4K FFM
set -euo pipefail
cd "$(dirname "$0")"

export TV_HOST="${TV_HOST:-192.168.1.10}"
PY=tools/venv/bin/python
[ -x "$PY" ] || PY=python3

"$PY" -I tools/toggle_theme.py "$@"
