FROM python:3.11.1

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
CMD [ "python", "-m", "src" ]
