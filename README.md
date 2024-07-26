# Dash powered Eurocontrol FRA Point viewer

Visualizes [Eurocontrol FRA Points](https://www.eurocontrol.int/publication/free-route-airspace-fra-points-list-ecac-area)

This small visualizer just uses a wrapper library in python for leaflet,
and shows FRA layers for each FRA Zone.

It automatically downloads the cycles available from eurocontrol, and will automatically refresh itself when a new file is published by eurocontrol

How to start:

```sh
    ## install used reqs
    pip install requirements.txt

    ## start the parser
    python main.py
```

The server will automatically launch.

How to run with docker:

```sh
    # build image
    ./build_image.bat

    #start in compose in daemon mode
    docker-compose up -d
```

### FAQ:

- **My Server takes a long first startup time, why?**

  Initially the server will download all currently available FRA files, which takes a while and parses its geojson.
  Should only be the first load, of the first user though!
