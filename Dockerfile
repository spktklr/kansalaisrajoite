FROM python:2.7-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src

COPY requirements.txt /src
COPY requirements-docker.txt /src
RUN pip install -r requirements.txt
RUN pip install -r requirements-docker.txt

COPY entrypoint.sh /src
COPY ./python /src

CMD sh /src/entrypoint.sh
