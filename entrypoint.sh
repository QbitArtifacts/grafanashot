#!/usr/bin/env bash


case $1 in
  service)
    flask run
    ;;
  *)
    shift
    venv/bin/python grafanashot.py $@
    ;;
esac