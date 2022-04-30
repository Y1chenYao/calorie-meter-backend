FROM python:3.7

RUN mkdir usr/app
WORKDIR usr/app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "app.py", "run", "--host=0.0.0.0"]

