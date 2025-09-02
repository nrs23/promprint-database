#!/bin/bash

while getopts ":-:" opt; do
    case $opt in
        -)
            case "${OPTARG}" in
                staging)
                    uv run gunicorn promprint.wsgi
                    ;;
                develop)
                    uv run python manage.py runserver
                    ;;
            esac
           ;;
    esac
done
