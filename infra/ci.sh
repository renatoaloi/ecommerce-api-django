#!/bin/bash

export TERM=xterm-256color

apt-get update && apt-get install -y jq
pip3 install awscli

if [[ ! `jq --version ` ]]; then
    echo "jq not found"
fi
apt install -y awscli

bash push.sh "$1"