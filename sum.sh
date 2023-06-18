#!/bin/bash
while true; do
    read -p "Enter URL (or press Enter to exit): " url
    if [ -z "$url" ]; then
        exit
    else
        python main.py -u "$url"
    fi
done
