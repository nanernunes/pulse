FROM        python:3.12-alpine

WORKDIR     /app

ADD         app/requirements.txt .

RUN         pip3 install --no-cache-dir -r requirements.txt

ADD         app/ .

CMD         ["python", "manage.py", "runserver", "0.0.0.0:8000"]