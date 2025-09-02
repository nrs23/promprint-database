#!/bin/bash

set -o allexport && source ./.env && set +o allexport

while getopts ":-:" opt; do
    case $opt in
        -)
            case "${OPTARG}" in
                staging)
                    docker compose up --build -d
                    ;;
                develop)
                    uv run python manage.py runserver $PORT
                    ;;
            esac
           ;;
    esac
done
