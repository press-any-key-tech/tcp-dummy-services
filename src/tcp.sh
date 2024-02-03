#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/code/tcp_dummy_services
python /code/tcp_dummy_services/tcp/ --host 0.0.0.0

