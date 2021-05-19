###########
# BUILDER #
###########

FROM python:3.9.4-alpine as builder

WORKDIR /usr/src/djRDO

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

# Needed by python mysql
RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev;

# Needed by postgresql
RUN apk add --no-cache postgresql-libs  &&\
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# Needed for argon2 password hashing and Pillow
RUN apk add gcc musl-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev zlib-dev 

RUN pip install --upgrade pip

# Copy djRDO folder
COPY . .

RUN pip install -r requirements.txt
# Slim down docker image
RUN apk --purge del .build-deps

ENTRYPOINT ["/usr/src/djRDO/docker_entrypoint.sh"]
