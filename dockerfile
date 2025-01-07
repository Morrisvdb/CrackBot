FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . ./app

CMD ["python3", "bot/main.py"]