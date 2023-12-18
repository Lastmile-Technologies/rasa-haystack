FROM rasa/rasa:latest
WORKDIR '/app'
#COPY . /app
USER root
# WORKDIR /app
# COPY . /app
#COPY ./data /app/data

#COPY requirements.txt .
COPY data /app/data
COPY config.yml /app
COPY credentials.yml /app
COPY data /app
COPY models /app
COPY domain.yml /app
COPY endpoints.yml /app
COPY requirements.txt /app
COPY socketChannel.py /app
COPY actions /app

#VOLUME /app/data
#VOLUME /app/models
RUN apt-get update && \
    apt-get install -y build-essential



RUN pip install --upgrade pip setuptools
RUN pip install --verbose --no-cache-dir -r requirements.txt
#RUN pip install -U setuptools wheel
RUN python -m spacy download en_core_web_md
RUN rasa train

CMD ["run","-m","/app/models","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]