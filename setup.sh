#!/bin/bash

# Setup auto linting at pre commit hook
chmod +x lint.sh
ln -s ../../lint.sh .git/hooks/pre-commit

# Create .env with new secret key
read -p "Secret key (can be anything but not empty): " key
echo "SECRET_KEY=${key}" > .env

# Create a venv and add dependencies
python3.13 -m venv .venv
source ./.venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements-local.txt