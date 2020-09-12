FROM python:3.6

ARG project_dir=/

ADD . $project_dir

WORKDIR $project_dir

RUN apt-get update

RUN apt-get install -y libgl1-mesa-dev

RUN pip install -r requirements.txt

ENV FLASK_APP /app.py

CMD flask run -h 0.0.0.0 -p $PORT