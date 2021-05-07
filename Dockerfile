FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /tmp

WORKDIR /tmp

COPY ./app /app

RUN pip install -r requirements.txt &&\
    cd / &&\
    mkdir conf &&\
    chmod -R 777 /conf\
    chmod -R 777 /app
