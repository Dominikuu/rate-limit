#!/bin/bash

image_name=rate-limit-server
tag=latest

docker build --no-cache -t ${image_name}:${tag:-latest} -f ./docker/Dockerfile .