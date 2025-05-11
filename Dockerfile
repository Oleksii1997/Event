FROM python:3.12.3

WORKDIR /usr/app

RUN apt-get update
RUN apt-get upgrade -y && apt-get -y install postgresql gcc python3-dev musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/app/requirements.txt
RUN pip install -r /usr/app/requirements.txt

COPY . /usr/app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]