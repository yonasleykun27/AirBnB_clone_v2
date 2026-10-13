#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""
from fabric.api import env, put, run
import os.path

env.hosts = ['100.25.19.204', '54.157.159.85']


def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        True if all operations succeeded, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = os.path.basename(archive_path)
        folder_name = archive_file.split(".")[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        put(archive_path, "/tmp/{}".format(archive_file))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_file, release_path))
        run("rm /tmp/{}".format(archive_file))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        return True
    except Exception:
        return False
