#!/usr/bin/env bash

export LIBGL_ALLOW_SOFTWARE=1
(cd simulations/control_client; python simulations/car/world.py)