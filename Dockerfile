FROM python:3.12

LABEL maintainer="ryan@ryanackley.com"

ADD src/ .

RUN python -m pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0 main:app
