#!/bin/sh

#build jq layer 
docker build -t jq-layer jq-layer
docker run --rm jq-layer cat /tmp/jq.zip > ./jq-layer.zip

#build graphicsmagick layer
export GM_VERSION=1.3.31
docker build --build-arg GM_VERSION -t gm-layer gm-layer
docker run --rm gm-layer cat /tmp/gm-${GM_VERSION}.zip > ./gm-layer.zip
