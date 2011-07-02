#!/usr/bin/env python

import sys
from collections import namedtuple
import lxml.etree
from lxml.builder import E

find_trkpt = lxml.etree.XPath('//gpx:trkpt',
    namespaces={'gpx': 'http://www.topografix.com/GPX/1/0'})
Point = namedtuple('Point', 'lat lon')

def iter_points():
    for gpx_path in sys.argv[1:]:
        with open(gpx_path) as gpx_file:
            gpx = lxml.etree.parse(gpx_file).getroot()
            for trkpt in find_trkpt(gpx):
                yield Point(trkpt.attrib['lat'], trkpt.attrib['lon'])

def main():
    osm = E.osm(version='0.6')
    for n, point in enumerate(iter_points()):
        node = E.node(id=str(n), visible='true', lat=point.lat, lon=point.lon)
        node.append(E.tag(k='name', v='gpx'))
        osm.append(node)
    osm.getroottree().write(sys.stdout, pretty_print=True)

if __name__ == '__main__':
    main()
