FROM python:3.11-slim

RUN apt-get update && apt-get install -y pkg-config

WORKDIR /apicode

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "python", "backend_app.py"]

