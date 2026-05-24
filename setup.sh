#!/bin/bash

# Setup linting script
chmod +x install-lint-hook.sh
./install-lint-hook.sh

# Clone the sample env
cp .env.example .env

# Create a venv and add dependencies
python3.13 -m venv .venv
source ./.venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements-local.txt

