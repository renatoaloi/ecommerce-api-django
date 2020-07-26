#!/bin/bash

export TERM=xterm-256color

if [[ ! `jq --version ` ]]; then
    echo "jq not found"
fi

sudo bash ./infra/push.sh "$1" "$2"