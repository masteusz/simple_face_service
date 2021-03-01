FROM python:3.8-slim

RUN apt-get update && \
    apt-get -y install build-essential gcc g++ python3-dev python3-opencv && \
    rm -rf /var/lib/apt/lists/*

# install requirements
COPY requirements.txt /app/requirements.txt

RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

# copy project files
COPY . /app
WORKDIR /app

RUN chmod a+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 8000
