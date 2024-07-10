#!/bin/bash

xhost +local:docker
docker run --rm \
  --net=host \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --device /dev/dri:/dev/dri \
  fossil-hunt