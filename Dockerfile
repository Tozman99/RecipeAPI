FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


#we use the package manager in order to install the postgres client 
# we update the registry and we use no-cache 
#in order to leave the cache empty
# and we install posgresql client 

#https://stackoverflow.com/questions/46221063/what-is-build-deps-for-apk-add-virtual-command/46222036
# for the explanation 
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
# we then delete this deps cause we no longer need them 

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user 

USER user

