#!/bin/bash


ACTION=${1:-get-data}


if [[ "$ACTION" != 'reset'* ]]; then
    echo "Waiting for 5 seconds..."
    sleep 5
    echo "Done."
    docker logs -t $(docker ps -a | grep "${ACTION:6}" | awk '{ print $1 }')
else
    docker rm $(docker ps -a | grep "${ACTION:6}" | awk '{ print $1 }')
    docker rmi $(docker images -a --filter "reference=*${ACTION:6}*" --format "{{.ID}}")

    cd notebooks
    if [[ "$ACTION" == 'reset-get-data' ]]; then
        cd get-data
    else
        cd eda
    fi

    cd notebooks

    rm -rf .ipynb_checkpoints/

    cd ../src
    rm -rf __pycache__/
fi
