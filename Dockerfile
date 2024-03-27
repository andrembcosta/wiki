FROM python:3.10-slim AS builder

WORKDIR /wiki_app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./encyclopedia ./encyclopedia 
COPY ./entries ./entries
COPY ./wiki ./wiki
COPY ./manage.py ./manage.py

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]