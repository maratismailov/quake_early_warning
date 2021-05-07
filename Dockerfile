FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY requirements.txt /tmp

COPY ./start.sh /start.sh

WORKDIR /tmp

COPY ./app /app

RUN pip install -r requirements.txt &&\
    cd / &&\
    mkdir conf &&\
    chmod -R 777 /conf &&\
    chmod -R 777 /app
