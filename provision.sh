#!/bin/bash
echo "
############################################################
## Development environment
## Machine: Ubuntu Server 14.04 LTS (e.g.: ami-f0b11187)
## User: $USER (e.g.: vagrant, ubuntu)
############################################################
"
if [ $# -lt 2 ]; then
    echo "Please provide following arguments:
## Mandatory:
##   $1 - Admin (e.g.: vagrant, ubuntu)
##   $2 - User (e.g.: svven, ducu, jon etc.)
## Optional:
##   $3 - User public key for SSH access (i.e. URL to id_rsa.pub)
##   $4 - User private key for deployment (i.e. URL to id_rsa)"
    exit 1
fi

## Make sure
cd /home/$1

## Common
sudo -u $1 -H bash /bootstrap/common/init.sh

## Add user
sudo -u $1 -H bash /bootstrap/common/adduser.sh $2

## Set ssh
sudo -u $2 -H bash /bootstrap/common/setssh.sh $3 $4

## Base app
sudo -u $2 -H bash /bootstrap/apps/baseapp.sh

if [ $4 ]; then
    ## Web app
    sudo -u $2 -H bash /bootstrap/apps/webapp.sh
fi
