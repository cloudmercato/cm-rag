FROM python:3.10
MAINTAINER Cloud Mercato

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /jc
COPY requirements.txt /jc/

RUN pip install -r requirements.txt
RUN mkdir -p /jc-data/

COPY . /jc/
COPY ./assets/docker-jc.json /etc/jc.json
COPY ./assets/system-prompt /jc-system-prompt

WORKDIR /jc/jc
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
