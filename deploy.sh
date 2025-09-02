#!/bin/bash

set -o allexport && source ./.env && set +o allexport

while getopts ":-:" opt; do
    case $opt in
        -)
            case "${OPTARG}" in
                staging)
                    uv run gunicorn --bind 127.0.0.1:$PORT promprint.wsgi
                    ;;
                develop)
                    uv run python manage.py runserver $PORT
                    ;;
            esac
           ;;
    esac
done
