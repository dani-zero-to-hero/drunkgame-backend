FROM python:3.11-alpine AS bare-drunk

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

FROM bare-drunk AS drunk

COPY drunk /app/drunk
COPY setup.py /app/
RUN pip install -e .

FROM drunk AS drunk-testing

COPY requirements.check.txt /app
COPY setup.cfg /app

COPY tests /app/tests

RUN pip install -r requirements.check.txt


