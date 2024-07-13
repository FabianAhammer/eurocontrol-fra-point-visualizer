# Python powered Eurocontrol FRA Point viewer

Visualizes [Eurocontrol FRA Points](https://www.eurocontrol.int/publication/free-route-airspace-fra-points-list-ecac-area)

This small visualizer just uses a wrapper library in python for leaflet,
and shows FRA layers for each FRA Zone.

Currently only uses the 2408 cycle file, can be customized

How to start:

```shell
    ## install used reqs
    pip install requirements.txt
        
    ## start the parser
    python main.py
```


How to create a custom FRA Point map:

- Place a .xlsx FRA Point file inside the `input` folder
- Start the Program
- Open the generated *.html file for the FRA Points
