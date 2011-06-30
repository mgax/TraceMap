"""
Hello! I'm a crawler. My job is to fetch GPS traces from OpenStreetMap. Other
scripts will make raster map tiles with traces, so JOSM users can load
them as a TMS layer, instead of downloading traces via the API.
"""

import logging
import urllib
import collections
import py.path

log = logging.getLogger('fetch')
log.setLevel(logging.DEBUG)

Parcel = collections.namedtuple('Parcel', 'left bottom page')

url_tmpl = ("http://api.openstreetmap.org/api/0.6/trackpoints"
            "?bbox=%(left).2f,%(bottom).2f,%(right).2f,%(top).2f"
            "&page=%(page)d")

class FetchOpener(urllib.FancyURLopener):
    version = ("GPS traces crawler, https://github.com/alex-morega/"
               "TraceMap/blob/master/crawler/fetch.py")


def get_gpx_page(bottom, left, top, right, page):
    url = url_tmpl % {
        'bottom': bottom,
        'left': left,
        'top': top,
        'right': right,
        'page': page,
    }
    log.debug("Fetching %s", url)
    return FetchOpener().open(url).read()


def get_gpx_parcel(parcel):
    return get_gpx_page(parcel.bottom, parcel.left,
                        parcel.bottom + 0.5, parcel.left + 0.5,
                        parcel.page)


class GpxArchive(object):
    def __init__(self, root_path):
        self.root_path = root_path

    def save_gpx_file(self, dir_name, page, data):
        file_path = self.root_path.join(dir_name, "%d.gpx" % page)
        log.debug("Saving to %r (%d KB)", str(file_path), len(data)/1024)
        file_path.dirpath().ensure(dir=True)
        file_path.write(data, 'wb')

    def save_gpx_parcel(self, parcel, data):
        dir_name = "%.2f,%.2f" % (parcel.left, parcel.bottom)
        self.save_gpx_file(dir_name, parcel.page, data)


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    #parser.add_argument('left')
    #parser.add_argument('bottom')
    parser.add_argument('-p', '--prefix', dest='prefix', required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    #parcel = Parcel(float(args.left), float(args.bottom), 1)
    #data = get_gpx_parcel(parcel)
    archive = GpxArchive(py.path.local(args.prefix))
    #archive.save_gpx_parcel(parcel, data)

    bottom, top = 45.7411, 45.8455
    left, right = 24.0428, 24.2378

    page = 1
    while True:
        data = get_gpx_page(bottom, left, top, right, page)
        if 'trkseg' not in data:
            break
        archive.save_gpx_file('sibiu', page, data)
        page += 1


if __name__ == '__main__':
    logging.basicConfig()
    main()
