#!/bin/bash

# Setup linting script
chmod +x install-lint-hook.sh
./install-lint-hook.sh

# Create .env with new secret key
read -p "Secret key (can be anything but not empty): " key
echo "SECRET_KEY=${key}" > .env

# Create a venv and add dependencies
python3.13 -m venv .venv
source ./.venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements-local.txt