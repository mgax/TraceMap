import logging

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

def main():
    get_gpx(26, 44.5, 1)

if __name__ == '__main__':
    logging.basicConfig()
    main()
