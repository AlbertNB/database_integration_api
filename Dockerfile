FROM python:3.10.5-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DB_HOST="127.0.0.1"
ENV DB_USER="user"
ENV DB_PASSWORD="password"
ENV DB_DATABASE="sample_db"

EXPOSE 5000

CMD [ "python", "app.py" ]
