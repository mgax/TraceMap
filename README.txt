importing data into PostgreSQL::

    osm2pgsql -d tracemap -S osm2pgsql-default.style data/sibiu-all.osm data/bucuresti-all.osm 

generating tiles::

    tilestache-seed.py -c tilestache.cfg -b 45.79 24.14 45.7901 24.1401 -p 1 -l postgis 16 -x
