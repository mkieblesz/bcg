FROM python:3.6

# install postgres client used by wait_for_db.sh script and nodejs for semantic
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -y postgresql-client-11

RUN mkdir /code
WORKDIR /code

ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY run.sh /
RUN chmod a+x /run.sh

COPY . /code

CMD ["/run.sh"]
