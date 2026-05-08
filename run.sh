#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${REPO_ROOT}/api/.venv/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "[ERROR] Missing api/.venv. Create it first:"
  echo "python -m venv api/.venv"
  echo "api/.venv/bin/python -m pip install -r api/requirements-modern.txt"
  exit 1
fi

"${PYTHON_BIN}" -m uvicorn app.main:app --app-dir "${REPO_ROOT}/api" --host 0.0.0.0 --port 8100 --reload
