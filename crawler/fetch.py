import logging
import urllib
import py.path

log = logging.getLogger('fetch')
log.setLevel(logging.DEBUG)

url_tmpl = ("http://api.openstreetmap.org/api/0.6/trackpoints"
            "?bbox=%(left).2f,%(bottom).2f,%(right).2f,%(top).2f"
            "&page=%(page)d")

def get_gpx(left, bottom, page):
    url = url_tmpl % {
        'bottom': bottom,
        'top': bottom + 0.5,
        'left': left,
        'right': left + 0.5,
        'page': page,
    }
    log.debug("Fetching %.2f,%.2f page %d: %s", left, bottom, page, url)
    return urllib.urlopen(url).read()


class GpxArchive(object):
    def __init__(self, root_path):
        self.root_path = root_path

    def save_gpx(self, left, bottom, page, data):
        dir_name = "%.2f,%.2f" % (left, bottom)
        file_name = "%d.gpx" % page
        dir_path = self.root_path.join(dir_name)
        dir_path.ensure(dir=True)
        dir_path.join(file_name).write(data)


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('left')
    parser.add_argument('bottom')
    parser.add_argument('-p', '--prefix', dest='prefix', required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    left = float(args.left)
    bottom = float(args.bottom)
    page = 1
    data = get_gpx(left, bottom, page)
    GpxArchive(py.path.local(args.prefix)).save_gpx(left, bottom, page, data)


if __name__ == '__main__':
    logging.basicConfig()
    main()
