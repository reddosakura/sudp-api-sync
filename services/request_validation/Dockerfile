FROM python:3.12-alpine

WORKDIR /Service

COPY . /Service/

RUN python3 -m pip install -r /Service/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
