FROM python:3.7
COPY . /code
WORKDIR /code
RUN pip install -r /code/requirements.txt
RUN mkdir -p /code/logs
RUN chmod 777 /code/logs
RUN chmod +x docker-entrypoint.sh
VOLUME ["/code/logs"]
CMD /code/docker-entrypoint.sh
