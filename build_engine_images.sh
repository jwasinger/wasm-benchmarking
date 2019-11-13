#! /bin/bash
set -e

(cd engines/wasmi && \
docker build -t localhost/wasmi . && \
docker build -t localhost/wasmi-instrumented -f Dockerfile.instrumented . )
