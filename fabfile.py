from fabric.api import env, local, cd, run, put, settings, hide
from fabric.contrib.files import exists
from local_fabfile import *

server_prefix = "/home/alexm/sites/maps.grep.ro"
server_repo = "%s/src/TraceMap" % server_prefix
server_www = "%s/www" % server_prefix
server_tiles = "%s/tiles" % server_prefix


def _push_code():
    local("git push -f 'redcoat:%s' HEAD:incoming" % server_repo)

def install_server():
    run("mkdir -p '%s'" % server_prefix)

    run("mkdir -p '%s'" % server_www)
    with cd(server_www):
        run("ln -s ../tiles")
        run("ln -s ../src/TraceMap/no-data.png")

    if not exists(server_repo):
        run("mkdir -p '%s'" % server_repo)
        with cd(server_repo):
            run("git init")
        _push_code()
        with cd(server_repo):
            run("git checkout incoming -b deploy")

    #with cd(server_prefix):
    #    run("virtualenv -p /usr/bin/python --distribute .")

def push():
    _push_code()
    with cd(server_repo):
        run("git reset incoming --hard")

def upload():
    from fabric.contrib.project import rsync_project
    run("mkdir -p '%s'" % server_tiles)
    rsync_project(server_tiles, "data/tiles/", delete=True)

def dbinit():
    db_name = "tracemap"
    postgis_share = "/usr/local/share/postgis"
    with settings(warn_only=True):
        local("dropdb '%s'" % db_name)
    with settings(hide('stdout')):
        local("createdb '%s'" % db_name)
        local("psql -d %s -f %s/postgis.sql" % (db_name, postgis_share))
        local("psql -d %s -f %s/spatial_ref_sys.sql" % (db_name, postgis_share))
