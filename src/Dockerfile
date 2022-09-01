# Dockerfile must be in the same level of folder

FROM python:3.7 
# instal python (base image)

RUN mkdir usr/app
# creating a dictory to put app.py db.py in
WORKDIR usr/app
# everything we do will be in this folder

COPY . .
# copy everything in the current directory to the working directory

RUN pip install -r requirements.txt

CMD python app.py
# tells the computer how to run app





