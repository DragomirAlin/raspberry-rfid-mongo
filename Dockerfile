
FROM python:3

WORKDIR /usr/app
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt
RUN pip install pymongo
COPY . /usr/app


CMD [ "python", "./rfid.py" ]