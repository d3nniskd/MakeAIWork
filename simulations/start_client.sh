#!/usr/bin/env bash

export LIBGL_ALLOW_SOFTWARE=1
(cd simulations/car; python ./hardcoded_client.py)