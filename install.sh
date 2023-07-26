#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

if [ "$SCRIPT_DIR" != "$PWD" ]; then
    cd "$SCRIPT_DIR" || exit 1
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    #shellcheck disable=SC1091
    source .venv/bin/activate
fi

pip install --editable .
