#!/usr/bin/env bash

# absolute path to the directory containing this script
SCRIPT_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# install venv
if [[ ! -d "$SCRIPT_SOURCE/venv" ]]; then
  python3 -m venv "$SCRIPT_SOURCE/venv"
fi

# use venv pip
PATH="$SCRIPT_SOURCE/venv/bin:$PATH"
pip install --upgrade pip setuptools wheel

# TODO add this file
if [[ -r "$SCRIPT_SOURCE/requirements.txt" ]]; then
  pip install --requirement "$SCRIPT_SOURCE/requirements.txt" --upgrade
fi

# symlink and start hc4-oled.service
ln -Ffs "$SCRIPT_SOURCE/hc4-oled.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now hc4-oled.service
