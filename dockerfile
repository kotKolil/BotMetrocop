FROM PYTHON:LATEST

WORKDIR /app

copy r.txt .

RUN pip3 install -r r.txt

COPY ..

CMD["python", "main.py"]
