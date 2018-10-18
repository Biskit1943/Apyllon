#!/bin/sh
source venv/bin/activate

# Try to init the database
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

# -u forwards all output to the docker-logs
exec python3 -u apyllon.py