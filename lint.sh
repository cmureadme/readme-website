#!/bin/bash

ruff check && ruff format
git add -u
exit 0
