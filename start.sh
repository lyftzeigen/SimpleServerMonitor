#!/bin/bash

cd "$(dirname "$0")"

touch ./ssm.log

export PYTHONPATH="${PYTHONPATH}:$(dirname "$0")"

/usr/bin/python3 ./ssm.py &>> ./ssm.log &