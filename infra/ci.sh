#!/bin/bash

export TERM=xterm-256color

sudo apt-get update
sudo apt-get install -y jq
sudo pip3 install awscli

if [[ ! `jq --version ` ]]; then
    echo "jq not found"
fi
sudo apt install -y awscli

sudo bash ./infra/push.sh "$1"