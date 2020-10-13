FROM python:3.8.5

WORKDIR /usr/src/app

COPY . .

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron
RUN touch /var/log/cron.log

COPY crontab /etc/cron.d/cjob
RUN chmod 0644 /etc/cron.d/cjob

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "sh", "./docker_start.sh" ]