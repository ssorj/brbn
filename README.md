# Brbn

Brbn serves HTTP requests

## Static embedding

    curl "https://raw.githubusercontent.com/ssorj/brbn/master/python/brbn.py" -o python/brbn.py

## Example script

    #!/bin/sh
    exec brbn --home "${SOMEAPP_HOME:-@someapp_home@}" "$@" someapp:Application
