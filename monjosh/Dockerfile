FROM python:3.8.0

WORKDIR /user/src/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
EXPOSE 80
ENTRYPOINT ["python", "app.py"]