#!/usr/bin/env bash

add-apt-repository ppa:ondrej/php
apt-get update
apt-get install -y apache2 php7.1
if ! [ -L /var/www/html ]; then
  rm -rf /var/www/html
  ln -fs /vagrant /var/www/html
fi
