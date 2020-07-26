#!/bin/bash

export TERM=xterm-256color

sudo apt-get update && apt-get install -y jq
pip3 install awscli

if [[ ! `jq --version ` ]]; then
    echo "jq not found"
fi
sudo apt install -y awscli

bash push.sh "$1"