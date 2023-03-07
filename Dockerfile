FROM python:3-slim-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]