FROM ubuntu:latest

WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y git python3.10 python3-pip
RUN pip3.10 install -r /app/requirements.txt
CMD ["python3.10", "/app/app.py"]
EXPOSE 5000