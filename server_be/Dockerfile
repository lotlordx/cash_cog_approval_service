#official Python runtime as a parent image
FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app/

ADD . .

# Celery configuration for supervisor
RUN mkdir -p /var/log/approval_service/celery_logs/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000