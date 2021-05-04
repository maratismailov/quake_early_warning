#!/bin/bash
`python3 -m venv env`
source env/bin/activate
pip install -U pip
pip install fastapi
pip install uvicorn
pip install aiofiles
pip install jinja2
pip install telegram-send
pip freeze -> requirements.txt
