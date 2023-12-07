FROM rasa/rasa:latest
WORKDIR '/app'
COPY . /app
USER root
# WORKDIR /app
# COPY . /app
COPY ./data /app/data

COPY requirements.txt .
VOLUME /app
VOLUME /app/data
VOLUME /app/models
RUN apt-get update && \
    apt-get install -y apparmor \
    apt-get install -y build-essential



RUN pip install --upgrade pip setuptools
RUN pip install --verbose --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_md
RUN rasa train

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]