FROM python:3.7-slim
WORKDIR /flaskapp
RUN apt-get update
RUN apt-get install libsndfile1 -y
RUN apt-get install ffmpeg -y
ADD ./flaskapp/ /flaskapp
ADD ./requirements.txt /flaskapp
RUN pip install -r requirements.txt
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:3680", "wsgi", "--timeout", "600"]