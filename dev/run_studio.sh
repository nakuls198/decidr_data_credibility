#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt
exec .venv/bin/streamlit run app.py --server.headless true --server.port "${PORT:-8501}"
