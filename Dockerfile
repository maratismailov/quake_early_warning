FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt /tmp

WORKDIR /tmp

RUN pip install -r requirements.txt &&\
    cd / &&\
    mkdir conf &&\
    chmod -R 777 /conf

COPY ./app /app