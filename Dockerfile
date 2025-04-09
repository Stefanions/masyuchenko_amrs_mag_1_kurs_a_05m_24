FROM python:3.9.13

WORKDIR /app

COPY app/ .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]