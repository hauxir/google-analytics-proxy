FROM python:3.6-slim

RUN pip install flask
RUN pip install requests
RUN pip install flask-cors
RUN pip install gunicorn

EXPOSE 5001

COPY app /app

WORKDIR /app

CMD gunicorn --bind 0.0.0.0:5001 wsgi:app --access-logfile -
