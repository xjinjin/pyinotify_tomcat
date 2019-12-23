#FROM python:3.7
#ADD requirements.txt /tmp/requirements.txt
#RUN pip install -r /tmp/requirements.txt
#RUN mkdir -p /code/logs
#RUN chmod 777 /code/logs
#WORKDIR /code
#COPY . /code
#RUN chmod +x docker-entrypoint.sh
#VOLUME ["/code/logs"]
##CMD /code/docker-entrypoint.sh

FROM python:3.7
WORKDIR /code
COPY . /code
RUN pip install -r /code/requirements.txt
RUN mkdir -p /code/logs
RUN chmod 777 /code/logs
RUN chmod +x docker-entrypoint.sh
#VOLUME ["/code/logs"]
#CMD /code/docker-entrypoint.sh
