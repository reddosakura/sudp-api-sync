FROM python:3.12-alpine

WORKDIR /car_passage

COPY . /car_passage

RUN python3 -m pip install -r /car_passage/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
