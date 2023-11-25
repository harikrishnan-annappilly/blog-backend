FROM python:3.9.18-slim-bullseye

RUN mkdir /flask-app

WORKDIR /flask-app

COPY ./req.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod 777 ./start.sh

CMD ["./start.sh"]
