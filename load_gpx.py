#!/usr/bin/env python

import sys
from collections import namedtuple
import lxml.etree

find_trkpt = lxml.etree.XPath('//gpx:trkpt',
    namespaces={'gpx': 'http://www.topografix.com/GPX/1/0'})
Point = namedtuple('Point', 'lat lon')

def iter_points():
    for gpx_path in sys.argv[1:]:
        with open(gpx_path) as gpx_file:
            gpx = lxml.etree.parse(gpx_file).getroot()
            for trkpt in find_trkpt(gpx):
                yield Point(trkpt.attrib['lat'], trkpt.attrib['lon'])

node_tmpl = """\
  <node id="%(id)d" lat="%(lat)s" visible="true" lon="%(lon)s">
    <tag k="name" v="gpx"/>
  </node>
"""

def main():
    out = sys.stdout
    out.write('<osm version="0.6">\n')
    for n, point in enumerate(iter_points()):
        out.write(node_tmpl % {'lat': point.lat, 'lon': point.lon, 'id': n})
    out.write('</osm>\n')

if __name__ == '__main__':
    main()
