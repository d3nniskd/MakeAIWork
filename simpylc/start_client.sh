#!/usr/bin/env bash

export LIBGL_ALLOW_SOFTWARE=1
(cd simulations/car/control_client; python3 ./hardcoded_client.py)