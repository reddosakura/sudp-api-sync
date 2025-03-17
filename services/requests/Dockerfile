FROM python:3.12-alpine

WORKDIR /requests

COPY . /requests/

RUN python3 -m pip install -r /requests/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
