importing data into PostgreSQL::

    osm2pgsql -d tracemap -S osm2pgsql-default.style data/sibiu-all.osm data/bucuresti-all.osm 

generating tiles::

    tilestache-seed.py -c tilestache.cfg -b ${box} -p 1 -l tracemap ${zooms}

bounding boxes:

sibiu
    45.7411 24.0428 45.8455 24.2378
bucurești
    44.30 25.88 44.61 26.31
