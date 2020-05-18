FROM python:3.6-alpine

RUN pip install --pre web.py

COPY src/ /app

WORKDIR /app

CMD ["python", "filler.py", "-a", "0.0.0.0", "-p", "8080", "-o", "/file.dat"]
