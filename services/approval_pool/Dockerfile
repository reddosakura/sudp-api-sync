FROM python:3.12-alpine

WORKDIR /approval_pool

COPY . /approval_pool

RUN python3 -m pip install -r /approval_pool/requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "web/app.py", "--port", "80"]
