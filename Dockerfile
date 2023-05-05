FROM python

RUN pip install redis fastapi uvicorn

WORKDIR /app

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
