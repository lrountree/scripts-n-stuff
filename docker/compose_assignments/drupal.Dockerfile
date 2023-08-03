# create your custom drupal image here, based of official drupal
ARG build_version=latest
FROM drupal:${build_version}
LABEL maintainer="lrountree" \
version="1.0" \
purpose="learning compose build"
ENV app_dir=/var/www/html/themes
RUN apt update \
&& apt install -y git
WORKDIR ${app_dir}
RUN git clone --depth 1 https://git.drupalcode.org/project/bootstrap.git \
&& chown -R www-data:www-data bootstrap
WORKDIR /var/www/html
