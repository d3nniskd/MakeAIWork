#!/usr/bin/env bash

export LIBGL_ALLOW_SOFTWARE=1
(cd simulations/control_client; python ./hardcoded_client.py)