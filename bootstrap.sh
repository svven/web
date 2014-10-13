#!/usr/bin/env bash

# PACKAGES
apt-get -y update
apt-get install -y linux-headers-$(uname -r) build-essential
apt-get install -y make libssl-dev zlib1g-dev libreadline-dev wget curl llvm
apt-get install -y libxml2-dev libxslt1-dev python-dev
apt-get install -y libbz2-dev bzip2 sqlite libsqlite3-dev
apt-get install -y curl git git-core
apt-get install -y python-pip python-setuptools
apt-get install -y nginx

easy_install virtualenv

# PYENV VIRTUALENV
git clone git://github.com/yyuu/pyenv.git /home/vagrant/.pyenv
git clone https://github.com/yyuu/pyenv-virtualenv.git /home/vagrant/.pyenv/plugins/pyenv-virtualenv
chown vagrant:vagrant /home/vagrant/.pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> /home/vagrant/.bashrc
echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bashrc

