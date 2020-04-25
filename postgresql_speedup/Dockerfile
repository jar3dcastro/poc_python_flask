FROM python:3.6-alpine
COPY requirements.txt /
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
CMD ["python", "main.py"]