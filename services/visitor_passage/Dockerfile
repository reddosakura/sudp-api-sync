FROM python:3.12-alpine

WORKDIR /visitor_passage

COPY . /visitor_passage/

RUN python3 -m pip install -r /visitor_passage/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
