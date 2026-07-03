#!/bin/bash
if docker network inspect main_net > /dev/null 2>&1; then
  echo "main_net already exists"
else
  docker network create --driver bridge --subnet 10.5.0.0/24 main_net
  echo "main_net created successfully"
fi
