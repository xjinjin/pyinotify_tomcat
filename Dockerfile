FROM python:3.7

COPY . /code
WORKDIR /code

RUN pip install -r /code/requirements.txt

RUN chmod +x docker-entrypoint.sh

CMD /code/docker-entrypoint.sh
