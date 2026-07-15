#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
venv_python="${project_root}/.venv/bin/python"

if [[ ! -x "${venv_python}" ]]; then
  python3 -m venv "${project_root}/.venv"
fi

"${venv_python}" "${project_root}/tools/download/download_public_sources.py"
