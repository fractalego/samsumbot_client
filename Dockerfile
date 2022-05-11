FROM python:3.8
RUN mkdir /app
RUN mkdir /app/client
RUN mkdir /app/src
RUN mkdir /app/deployment

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt update
RUN apt install -y python3 python3-pip
RUN apt install -y nodejs npm
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --upgrade requests

COPY ./src/ /app/src/
COPY ./client/ /app/client/
COPY ./deployment/ /app/deployment/
COPY knowledge.yaml /app/
COPY config-for-docker-image.yaml /app/config.yaml

RUN npm run build --prefix client
CMD ["bash", "deployment/download_models_and_start_server.sh"]
