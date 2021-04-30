#!/bin/bash
`python3 -m venv env`
source env/bin/activate
pip install -U pip
pip install fastapi
pip install uvicorn
pip install pytelegrambotapi
pip freeze -> requirements.txt
