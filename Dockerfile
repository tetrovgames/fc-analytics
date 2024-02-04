FROM python:3.12.1-alpine3.19

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./run.sh /code/run.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV PORT 80

RUN chmod +x run.sh
CMD ["./run.sh"]
