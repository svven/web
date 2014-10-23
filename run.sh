#!/bin/bash
echo '['`date +"%d/%m/%Y %H:%M:%S"`'] Run gunicorn'

cd
# exec bin/gunicorn -c conf/gunicorn.conf.py wsgi:application
