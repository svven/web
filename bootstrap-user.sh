#!/usr/bin/env bash

source /home/vagrant/.bashrc
export PATH="/home/vagrant/.pyenv/bin:/home/vagrant/.pyenv/shims:$PATH"
eval "$(pyenv init -)"

pyenv install 2.7.7
pyenv rehash
pyenv global 2.7.7
pyenv virtualenv 2.7.7 svven-web 

mkdir -p /home/vagrant/svven/

printf "Host bitbucket.org\n  HostName bitbucket.org\n  IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config
ssh-keygen -R bitbucket.org
ssh-keyscan bitbucket.org >> /home/vagrant/.ssh/known_hosts
ssh-keygen -R github.com
ssh-keyscan github.com >> /home/vagrant/.ssh/known_hosts

cd ~/svven/
git clone git@bitbucket.org:svven/web.git

mkdir ~/svven/web/logs
cd ~/svven/web/sources
pyenv local svven-web

pip install -r requirements.txt 
pip install git+https://github.com/svven/tweepy.git#egg=tweepy # TO GET 2.4?

pip install gunicorn
pip install flask

export GUNC_ACCESS_LOG=~/svven/web/logs/guncacc.log
export GUNC_LOG=~/svven/web/logs/gunc.log

sudo cp conf/nginx.conf /etc/nginx/

sudo service nginx start

gunicorn --access-logfile $GUNC_ACCESS_LOG --log-file $GUNC_LOG --log-level debug run:app -b 0.0.0.0:8000 &


