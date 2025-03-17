FROM python:3.12-alpine

WORKDIR /users

COPY . /users

RUN python3 -m pip install -r /users/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
