FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements/requirements.txt ./requirements/requirements.txt
RUN pip3 install -r requirements/requirements.txt

COPY ./app /app

CMD [ "uvicorn", "app.main:app", "--reload","--host", "0.0.0.0", "--port", "8080"]
