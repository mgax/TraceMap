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

def get_gpx(parcel):
    url = url_tmpl % {
        'bottom': parcel.bottom,
        'top': parcel.bottom + 0.5,
        'left': parcel.left,
        'right': parcel.left + 0.5,
        'page': parcel.page,
    }
    log.debug("Fetching %r: %s", parcel, url)
    return urllib.urlopen(url).read()


class GpxArchive(object):
    def __init__(self, root_path):
        self.root_path = root_path

    def save_gpx(self, parcel, data):
        dir_name = "%.2f,%.2f" % (parcel.left, parcel.bottom)
        file_name = "%d.gpx" % parcel.page
        file_path = self.root_path.join(dir_name, file_name)
        log.debug("Saving %r to %r (%d KB)",
                  parcel, str(file_path), len(data)/1024)
        file_path.dirpath().ensure(dir=True)
        file_path.write(data)


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('left')
    parser.add_argument('bottom')
    parser.add_argument('-p', '--prefix', dest='prefix', required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    parcel = Parcel(float(args.left), float(args.bottom), 1)
    data = get_gpx(parcel)
    GpxArchive(py.path.local(args.prefix)).save_gpx(parcel, data)


if __name__ == '__main__':
    logging.basicConfig()
    main()
