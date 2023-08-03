# Udemy docker course, dockerfile assignment 1

ARG build_version=6-alpine
FROM node:${build_version}
LABEL maintainer="lrountree" \
version="1.0" \
purpose="learning exercise"
ENV app_dir=/usr/src/app
EXPOSE 3000
RUN apk add --update tini \
&& mkdir -p ${app_dir}
WORKDIR ${app_dir}
COPY package.json .
COPY app.js .
COPY bin bin
COPY public public
COPY routes routes
COPY views views
RUN npm install \ 
&& npm cache clean --force
CMD /sbin/tini -- node ./bin/www
