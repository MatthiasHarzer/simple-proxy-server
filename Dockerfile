FROM python:3.12

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install uvicorn

CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]
