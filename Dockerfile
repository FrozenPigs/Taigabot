FROM alpine
RUN apk add \
        python2 \
        gcc \
        g++ \
        python2-dev \
        libxml2 \
        libxml2-dev \
        libxslt-dev \
        enchant2 \
        enchant2-dev && \
    python2 -m ensurepip

WORKDIR /home/taigabot
COPY ./requirements.txt ./requirements.txt
RUN python2 -m pip install -r requirements.txt
COPY ./requirements_extra.txt ./requirements_extra.txt
RUN python2 -m pip install -r requirements_extra.txt
COPY ./ ./

CMD [ "python2", "./bot.py" ]
