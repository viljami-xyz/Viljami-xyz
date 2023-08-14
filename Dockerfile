FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Install cron and other necessary tools
RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY ./compose/cronjob /etc/cron.d/cronjob
COPY ./compose/update_db.sh /app/update_db.sh

RUN chmod +x /app/update_db.sh

RUN chmod 0644 /etc/cron.d/cronjob && crontab /etc/cron.d/cronjob

RUN service cron start

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app/app
